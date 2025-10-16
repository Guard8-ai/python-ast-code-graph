#!/usr/bin/env python3
"""
Integration Mapper: Generates hierarchical JSON maps showing EVERY connection
between Python codebase components.

Three-phase architecture:
1. Hierarchy Building: Tree structure with FQN assignment
2. Integration Extraction: Rich edges (imports, calls, attributes, inheritance)
3. Flow & Crossroad Analysis: Data flows, crossroads, critical paths
"""

import ast
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Set, Optional, Tuple
from collections import defaultdict
from datetime import datetime


# ============================================================================
# PHASE 1: HIERARCHY BUILDING
# ============================================================================

class HierarchyBuilder(ast.NodeVisitor):
    """Build hierarchical tree structure with FQN assignment."""

    def __init__(self):
        self.tree: Dict[str, Any] = {}
        self.symbol_table: Dict[str, Dict[str, Any]] = {}
        self.scope_stack: List[str] = []  # [package, module, class, function]
        self.current_module: Optional[str] = None
        self.alias_map: Dict[str, str] = {}
        self.imports_in_module: List[Dict[str, Any]] = []

    def get_current_fqn(self) -> str:
        """Get fully qualified name for current scope."""
        return ".".join(self.scope_stack)

    def register_node(self, node_type: str, name: str, node: ast.AST,
                      parent_fqn: str = "") -> str:
        """Register a node in symbol table and return its FQN."""
        fqn = f"{parent_fqn}.{name}" if parent_fqn else name

        # Handle Module nodes which don't have lineno
        if isinstance(node, ast.Module):
            line_range = [1, 1]
        else:
            line_range = [node.lineno, node.end_lineno or node.lineno]

        docstring = ast.get_docstring(node)

        self.symbol_table[fqn] = {
            "type": node_type,
            "fqn": fqn,
            "name": name,
            "line_range": line_range,
            "path": self.current_module,
            "docstring": docstring,
            "children": {},
            "imports": self.imports_in_module if node_type == "module" else [],
        }

        return fqn

    def visit_Module(self, node: ast.Module) -> None:
        """Process module and set up scope."""
        # Extract module FQN from path
        module_fqn = self.current_module.replace("/", ".").replace(".py", "")

        # Register module
        self.register_node("module", module_fqn, node)
        self.scope_stack = [module_fqn]

        # Add to tree
        parts = module_fqn.split(".")
        current = self.tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {"type": "package", "children": {}}
            current = current[part]["children"]

        current[parts[-1]] = self.symbol_table[module_fqn]

        # Visit all children
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Process class definition."""
        parent_fqn = self.get_current_fqn()
        class_fqn = self.register_node("class", node.name, node, parent_fqn)

        # Track base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(self._extract_attribute_fqn(base))

        self.symbol_table[class_fqn]["bases"] = bases
        self.symbol_table[class_fqn]["methods"] = {}
        self.symbol_table[class_fqn]["attributes"] = {}

        # Register class in parent (only if parent exists)
        if parent_fqn in self.symbol_table:
            self.symbol_table[parent_fqn]["children"][node.name] = class_fqn

        # Push scope and visit
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Process function or method."""
        parent_fqn = self.get_current_fqn()
        func_fqn = self.register_node("function", node.name, node, parent_fqn)

        # Extract parameters
        params = []
        for arg in node.args.args:
            params.append({"name": arg.arg, "type": None})

        self.symbol_table[func_fqn]["parameters"] = params
        self.symbol_table[func_fqn]["return_type"] = None
        self.symbol_table[func_fqn]["calls"] = []
        self.symbol_table[func_fqn]["reads_attributes"] = []
        self.symbol_table[func_fqn]["writes_attributes"] = []

        # Register in parent (only if parent exists)
        if parent_fqn in self.symbol_table:
            if len(self.scope_stack) >= 2 and self.scope_stack[-1] != self.current_module:
                # This is a method
                parent_class_fqn = self.scope_stack[-1]
                if parent_class_fqn in self.symbol_table:
                    self.symbol_table[parent_class_fqn]["methods"][node.name] = func_fqn
            else:
                # This is a module-level function
                self.symbol_table[parent_fqn]["children"][node.name] = func_fqn

        # Don't visit nested functions deeply
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Process async function (same as FunctionDef)."""
        self.visit_FunctionDef(node)  # type: ignore

    def _extract_attribute_fqn(self, node: ast.Attribute) -> str:
        """Extract FQN from attribute chain like obj.a.b.c."""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))


# ============================================================================
# PHASE 2: INTEGRATION EXTRACTION
# ============================================================================

class IntegrationExtractor(ast.NodeVisitor):
    """Extract rich integration edges (imports, calls, attributes, inheritance)."""

    def __init__(self, symbol_table: Dict[str, Dict[str, Any]]):
        self.symbol_table = symbol_table
        self.scope_stack: List[str] = []
        self.current_module: Optional[str] = None
        self.alias_map: Dict[str, str] = {}
        self.integration_edges: List[Dict[str, Any]] = []
        self.call_graph: Dict[str, List[str]] = defaultdict(list)

    def visit_Module(self, node: ast.Module) -> None:
        """Set up module scope."""
        module_fqn = self.current_module.replace("/", ".").replace(".py", "")
        self.scope_stack = [module_fqn]
        self.alias_map.clear()
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Process import statements."""
        for alias in node.names:
            module_name = alias.name
            as_name = alias.asname or alias.name
            self.alias_map[as_name] = module_name

            edge = {
                "type": "import",
                "source": self.get_current_fqn(),
                "target": module_name,
                "items": [as_name],
                "line": node.lineno,
                "integration_type": "import_module"
            }
            self.integration_edges.append(edge)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Process from...import statements."""
        if node.module is None:
            return

        items = []
        for alias in node.names:
            items.append(alias.name)
            as_name = alias.asname or alias.name
            self.alias_map[as_name] = f"{node.module}.{alias.name}"

        edge = {
            "type": "import",
            "source": self.get_current_fqn(),
            "target": node.module,
            "items": items,
            "line": node.lineno,
            "integration_type": "import_from"
        }
        self.integration_edges.append(edge)

    def visit_Call(self, node: ast.Call) -> None:
        """Process function calls."""
        target_fqn = self._resolve_call_target(node.func)

        # Extract arguments
        args = []
        for arg in node.args:
            args.append({"type": "positional", "value": ast.unparse(arg)})
        for keyword in node.keywords:
            args.append({"type": "keyword", "name": keyword.arg, "value": ast.unparse(keyword.value)})

        edge = {
            "type": "call",
            "source": self.get_current_fqn(),
            "target": target_fqn,
            "target_fqn": target_fqn,
            "line": node.lineno,
            "args": args,
            "integration_type": "function_call"
        }

        self.integration_edges.append(edge)
        self.call_graph[target_fqn].append(self.get_current_fqn())

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Process attribute access (read/write)."""
        # Determine if this is a read or write
        is_write = isinstance(node.ctx, ast.Store)

        fqn = self._extract_attribute_fqn(node)

        edge = {
            "type": "attribute",
            "source": self.get_current_fqn(),
            "target": fqn,
            "access": "write" if is_write else "read",
            "line": node.lineno,
            "integration_type": "attribute_access"
        }

        self.integration_edges.append(edge)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Extract inheritance information."""
        class_fqn = f"{self.get_current_fqn()}.{node.name}"

        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_fqn = self.alias_map.get(base.id, base.id)
                bases.append(base_fqn)
            elif isinstance(base, ast.Attribute):
                base_fqn = self._extract_attribute_fqn(base)
                bases.append(base_fqn)

        if bases:
            edge = {
                "type": "inheritance",
                "source": class_fqn,
                "targets": bases,
                "line": node.lineno,
                "integration_type": "inheritance"
            }
            self.integration_edges.append(edge)

        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def get_current_fqn(self) -> str:
        """Get current FQN."""
        return ".".join(self.scope_stack) if self.scope_stack else ""

    def _resolve_call_target(self, func: ast.expr) -> str:
        """Resolve function call target to FQN."""
        if isinstance(func, ast.Name):
            return self.alias_map.get(func.id, func.id)
        elif isinstance(func, ast.Attribute):
            return self._extract_attribute_fqn(func)
        else:
            return "<dynamic_call>"

    def _extract_attribute_fqn(self, node: ast.Attribute) -> str:
        """Extract FQN from attribute chain."""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))


# ============================================================================
# PHASE 3: FLOW & CROSSROAD ANALYSIS
# ============================================================================

class FlowAnalyzer:
    """Analyze data flows and detect crossroads."""

    def __init__(self, integration_edges: List[Dict[str, Any]],
                 call_graph: Dict[str, List[str]]):
        self.integration_edges = integration_edges
        self.call_graph = call_graph
        self.crossroads: List[Dict[str, Any]] = []
        self.critical_paths: List[Dict[str, Any]] = []

    def analyze(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Run flow analysis."""
        self._detect_crossroads()
        self._identify_critical_paths()
        return self.crossroads, self.critical_paths

    def _detect_crossroads(self) -> None:
        """Detect module boundary crossroads."""
        module_interactions: Dict[Tuple[str, str], int] = defaultdict(int)

        for edge in self.integration_edges:
            source = edge.get("source", "")
            target = edge.get("target", "")

            # Extract module names
            source_module = source.split(".")[0] if source else ""
            target_module = target.split(".")[0] if target else ""

            if source_module and target_module and source_module != target_module:
                key = tuple(sorted([source_module, target_module]))
                module_interactions[key] += 1

        # Create crossroads
        for (module_a, module_b), count in sorted(module_interactions.items(),
                                                    key=lambda x: x[1], reverse=True):
            if count >= 3:  # Only include significant crossroads
                self.crossroads.append({
                    "id": f"{module_a}_{module_b}_junction",
                    "components": [module_a, module_b],
                    "integration_count": count,
                    "criticality": "high" if count > 10 else "medium"
                })

    def _identify_critical_paths(self) -> None:
        """Identify critical data flow paths."""
        # For now, just identify high-call-count functions as entry points
        call_counts = defaultdict(int)
        for edges in self.call_graph.values():
            for caller in edges:
                call_counts[caller] += 1

        # Top callers are entry points of critical paths
        for func, count in sorted(call_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            if count >= 2:
                self.critical_paths.append({
                    "id": f"path_{func.replace('.', '_')}",
                    "entry_point": func,
                    "call_count": count,
                    "complexity": "high" if count > 5 else "medium"
                })


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

class IntegrationMapper:
    """Main orchestrator for three-phase analysis."""

    def __init__(self, root_path: Path, exclude_patterns: Optional[List[str]] = None):
        self.root_path = root_path
        self.exclude_patterns = exclude_patterns or []
        self.files: List[Path] = []
        self.symbol_table: Dict[str, Dict[str, Any]] = {}
        self.tree: Dict[str, Any] = {}
        self.integration_edges: List[Dict[str, Any]] = []

    def discover_files(self) -> None:
        """Discover all Python files."""
        python_files = list(self.root_path.rglob("*.py"))
        self.files = [f for f in python_files if not any(
            pattern in str(f) for pattern in self.exclude_patterns
        )]
        print(f"Discovered {len(self.files)} Python files")

    def phase1_build_hierarchy(self) -> None:
        """Phase 1: Build hierarchy with FQN assignment."""
        print("Phase 1: Building hierarchy...")

        for file_path in self.files:
            try:
                with open(file_path, 'r') as f:
                    source = f.read()

                tree = ast.parse(source)

                # Build hierarchy
                builder = HierarchyBuilder()
                module_path = str(file_path.relative_to(self.root_path))
                builder.current_module = module_path
                builder.visit(tree)

                self.symbol_table.update(builder.symbol_table)
                self.tree.update(builder.tree)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        print(f"Built hierarchy with {len(self.symbol_table)} components")

    def phase2_extract_integration(self) -> None:
        """Phase 2: Extract rich integration edges."""
        print("Phase 2: Extracting integration points...")

        for file_path in self.files:
            try:
                with open(file_path, 'r') as f:
                    source = f.read()

                tree = ast.parse(source)

                # Extract integration
                extractor = IntegrationExtractor(self.symbol_table)
                module_path = str(file_path.relative_to(self.root_path))
                extractor.current_module = module_path
                extractor.visit(tree)

                self.integration_edges.extend(extractor.integration_edges)

            except Exception as e:
                print(f"Error extracting integration from {file_path}: {e}")

        print(f"Extracted {len(self.integration_edges)} integration edges")

    def phase3_analyze_flows(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Phase 3: Analyze flows and crossroads."""
        print("Phase 3: Analyzing flows and crossroads...")

        # Build call graph for flow analysis
        call_graph: Dict[str, List[str]] = defaultdict(list)
        for edge in self.integration_edges:
            if edge.get("type") == "call":
                call_graph[edge.get("target", "")].append(edge.get("source", ""))

        analyzer = FlowAnalyzer(self.integration_edges, call_graph)
        crossroads, critical_paths = analyzer.analyze()

        print(f"Identified {len(crossroads)} crossroads and {len(critical_paths)} critical paths")

        return crossroads, critical_paths

    def build_output(self, crossroads: List[Dict[str, Any]],
                     critical_paths: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build final output JSON."""
        return {
            "metadata": {
                "total_integration_points": len(self.integration_edges),
                "total_crossroads": len(crossroads),
                "analysis_timestamp": datetime.now().isoformat(),
                "files_analyzed": len(self.files),
                "components_found": len(self.symbol_table)
            },
            "codebase_tree": self.tree,
            "global_integration_map": {
                "crossroads": crossroads,
                "critical_paths": critical_paths,
                "data_flows": [],
                "statistics": {
                    "total_components": len(self.symbol_table),
                    "total_integration_points": len(self.integration_edges)
                }
            }
        }

    def run(self) -> Dict[str, Any]:
        """Run complete analysis."""
        print(f"\n🚀 Starting Integration Mapper Analysis")
        print(f"Root: {self.root_path}\n")

        self.discover_files()
        self.phase1_build_hierarchy()
        self.phase2_extract_integration()
        crossroads, critical_paths = self.phase3_analyze_flows()

        return self.build_output(crossroads, critical_paths)


# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Integration Mapper: Generate hierarchical integration maps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python integration_mapper.py --root ./myproject --output map.json
  python integration_mapper.py --root . --exclude "*/tests/*" --exclude "*/migrations/*"
        """
    )

    parser.add_argument("--root", required=True, help="Root directory of codebase")
    parser.add_argument("--output", default="integration_map.json", help="Output JSON file")
    parser.add_argument("--exclude", action="append", help="Glob pattern to exclude")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    root_path = Path(args.root)
    if not root_path.exists():
        print(f"❌ Root path not found: {root_path}")
        return 1

    mapper = IntegrationMapper(root_path, args.exclude)
    output = mapper.run()

    # Write output
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Analysis complete!")
    print(f"Output: {output_path}")
    print(f"Integration points: {output['metadata']['total_integration_points']}")
    print(f"Crossroads: {output['metadata']['total_crossroads']}\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
