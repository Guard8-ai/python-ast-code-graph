"""
VerboseFormatter: Default output format with full component and edge details.

This formatter maintains backward compatibility with the existing integration map
output format. It includes all metadata, maintains hierarchical structure, and
preserves full information about components and edges.

Output characteristics:
- Full hierarchical codebase tree
- Complete edge objects with all metadata
- Preserves all docstrings and metadata
- ~190K tokens for typical projects
- Default format (no compression)

Example:
    >>> from verbose_formatter import VerboseFormatter
    >>>
    >>> formatter = VerboseFormatter()
    >>> output = formatter.build_output(symbol_table, edges, metadata)
    >>> # Output includes full tree and all edge details
"""

from typing import Dict, Any, List
from .base_formatter import BaseFormatter


class VerboseFormatter(BaseFormatter):
    """Output formatter for verbose (full-detail) integration maps.

    This is the default formatter that maintains backward compatibility with
    the original integration map output format. It includes complete information
    about all components and edges without compression.

    Methods implement the BaseFormatter interface to produce verbose output.
    """

    def format_components(self, symbol_table: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Format components as full hierarchical tree.

        Builds a hierarchical tree structure from the symbol table, maintaining
        all package/module/class relationships and metadata.

        Args:
            symbol_table: Dictionary mapping FQN strings to component metadata

        Returns:
            Hierarchical tree dict suitable for JSON serialization. Structure:
            {
                "package_name": {
                    "type": "package",
                    "children": {
                        "module_name": {
                            "type": "module",
                            "fqn": "package.module_name",
                            "name": "module_name",
                            "path": "package/module_name.py",
                            "line_range": [1, 100],
                            "docstring": "...",
                            "children": {...},
                            "imports": [...]
                        },
                        ...
                    }
                },
                ...
            }

        Note:
            This method reconstructs the hierarchical tree from the flat symbol_table.
            All component metadata is preserved in the output.
        """
        tree: Dict[str, Any] = {}

        for fqn, component in symbol_table.items():
            # Skip if component already processed (as child of another component)
            if any(fqn.startswith(other_fqn + ".") for other_fqn in symbol_table if other_fqn != fqn):
                continue

            # Build path to this component
            parts = fqn.split(".")

            # Navigate/create tree structure
            current = tree
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {
                        "type": "package",
                        "children": {}
                    }
                elif "children" not in current[part]:
                    current[part]["children"] = {}

                current = current[part]["children"]

            # Add the component itself
            current[parts[-1]] = {
                **component,
                "children": component.get("children", {})
            }

        return tree

    def format_edges(self, edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format edges as full objects with all metadata.

        Returns edges exactly as provided, maintaining all details.

        Args:
            edges: List of integration edge dictionaries

        Returns:
            Same list of edges (no transformation for verbose mode)

        Note:
            Verbose mode preserves all edge information without any compression
            or filtering.
        """
        return edges

    def build_output(self, symbol_table: Dict[str, Dict[str, Any]],
                     edges: List[Dict[str, Any]],
                     metadata: Dict[str, Any],
                     crossroads: List[Dict[str, Any]] = None,
                     critical_paths: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build complete verbose output structure.

        Assembles the verbose format output by combining formatted components,
        edges, and analysis results. This maintains the original output format
        for backward compatibility.

        Args:
            symbol_table: Dictionary mapping FQN strings to component metadata
            edges: List of integration edge dictionaries
            metadata: Analysis metadata dict with statistics
            crossroads: List of identified crossroads (optional)
            critical_paths: List of critical paths (optional)

        Returns:
            Complete verbose output dict:
            {
                "metadata": {
                    "total_integration_points": int,
                    "total_crossroads": int,
                    "analysis_timestamp": str,
                    "files_analyzed": int,
                    "components_found": int
                },
                "codebase_tree": {...},  # Full hierarchical tree
                "global_integration_map": {
                    "crossroads": [...],
                    "critical_paths": [...],
                    "data_flows": [...],
                    "statistics": {...}
                }
            }

        Note:
            This format is verbose and token-intensive (~190K tokens typical).
            Use CompactFormatter for context-aware applications.
        """
        if crossroads is None:
            crossroads = []
        if critical_paths is None:
            critical_paths = []

        # Format components and edges
        tree = self.format_components(symbol_table)
        formatted_edges = self.format_edges(edges)

        # Build complete output structure
        return {
            "metadata": metadata,
            "codebase_tree": tree,
            "global_integration_map": {
                "crossroads": crossroads,
                "critical_paths": critical_paths,
                "data_flows": [],
                "statistics": {
                    "total_components": len(symbol_table),
                    "total_integration_points": len(formatted_edges),
                    "total_edges": len(formatted_edges)
                }
            },
            "integration_edges": formatted_edges
        }

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate verbose output structure.

        Checks that output contains required top-level keys.

        Args:
            output: Output dictionary to validate

        Returns:
            True if output is valid, False otherwise
        """
        required_keys = {"metadata", "codebase_tree", "global_integration_map"}
        return all(key in output for key in required_keys)
