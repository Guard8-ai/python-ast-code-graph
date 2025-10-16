"""CompactFormatter: Produces token-efficient compressed output.

Implements context-aware mode that reduces 190K tokens to <30K tokens
through intelligent compression focused on crossroads analysis.

Key principle: Store ANALYSIS (crossroads, critical paths), not raw edges.
"""

import json
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from ..utils.indexer import ComponentIndexer
from ..utils.abbreviations import (
    abbreviate_keys,
    abbreviate_type,
    abbreviate_integration,
    TYPE_CODES,
    INTEGRATION_CODES,
)
from ..utils.json_writer import write_compact_json


class CompactFormatter:
    """Context-aware formatter producing <30K token output.

    Compression strategy:
    1. Flatten component hierarchy (parent IDs instead of nesting)
    2. Use integer IDs for FQNs (60% reduction)
    3. Abbreviate all keys (20% reduction)
    4. Focus on crossroads analysis, not raw edges (most important!)
    5. Minify JSON output (30% reduction)

    Output structure:
    {
        "v": "2.0-compact",
        "meta": {...},           # Abbreviated metadata
        "idx": {"1": "fqn", ...},  # Component index
        "cmp": [...],            # Flat components (abbreviated)
        "crd": [...],            # Crossroads analysis
        "cp": [...]              # Critical paths
    }
    """

    def __init__(self) -> None:
        """Initialize formatter with component indexer."""
        self.indexer = ComponentIndexer()

    def format_output(self, verbose_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert verbose output to compact format.

        Args:
            verbose_output: Original verbose format output

        Returns:
            Compact format dictionary
        """
        # Extract sections
        metadata = verbose_output.get("metadata", {})
        tree = verbose_output.get("codebase_tree", {})
        integration_map = verbose_output.get("global_integration_map", {})

        # Step 1: Flatten component hierarchy
        flat_components = self._flatten_hierarchy(tree)

        # Step 2: Abbreviate keys
        flat_components_abbr = abbreviate_keys(flat_components)

        # Step 3: Extract and compress crossroads
        crossroads = integration_map.get("crossroads", [])
        crossroads_abbr = self._compress_crossroads(crossroads)

        # Step 4: Extract and compress critical paths
        critical_paths = integration_map.get("critical_paths", [])
        critical_paths_abbr = self._compress_critical_paths(critical_paths)

        # Step 5: Create metadata section
        meta_abbr = self._compress_metadata(metadata)

        # Step 6: Assemble output
        output = {
            "v": "2.0-compact",
            "meta": meta_abbr,
            "idx": self.indexer.to_json_index(),  # ID → FQN mapping
            "cmp": flat_components_abbr,  # Compressed components
            "crd": crossroads_abbr,  # Crossroads analysis
            "cp": critical_paths_abbr,  # Critical paths
        }

        return output

    def _flatten_hierarchy(self, tree: Dict[str, Any], parent_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Flatten nested hierarchy to component list with parent IDs.

        Before (nested): 8 levels deep, massive duplication
        After (flat): Single list with parent IDs

        Token savings: ~60% through structure flattening
        """
        components = []

        def traverse(node: Dict[str, Any], node_name: str, parent_id_val: Optional[int]) -> None:
            """Recursively traverse hierarchy."""
            # Get FQN
            if isinstance(node, dict):
                fqn = node.get("fqn")
                if not fqn:
                    # Build FQN from path
                    node_type = node.get("type", "package")
                    fqn = node_name

                # Create ID
                comp_id = self.indexer.get_or_create_id(fqn)

                # Create component entry
                component: Dict[str, Any] = {
                    "id": comp_id,
                    "t": abbreviate_type(node.get("type", "package")),
                    "n": node_name,
                }

                # Add parent if exists
                if parent_id_val is not None:
                    component["p"] = parent_id_val

                # Add optional fields only if present
                if "line_range" in node:
                    component["lr"] = node["line_range"]

                if "docstring" in node and node["docstring"]:
                    # Truncate docstring to first 50 chars
                    doc = node["docstring"][:50]
                    if len(node["docstring"]) > 50:
                        doc += "..."
                    component["doc"] = doc

                # Add method/attribute count if relevant
                if "methods" in node:
                    component["m_ct"] = len(node["methods"])
                if "attributes" in node:
                    component["a_ct"] = len(node["attributes"])

                components.append(component)

                # Traverse children
                for child_name, child_node in node.get("children", {}).items():
                    traverse(child_node, child_name, comp_id)

        # Process tree
        for root_name, root_node in tree.items():
            traverse(root_node, root_name, None)

        return components

    def _compress_crossroads(self, crossroads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compress crossroads analysis.

        Crossroads are module boundary interaction points - the KEY insight of the
        integration mapper. Store these efficiently.
        """
        compressed = []

        for crossroad in crossroads:
            # Get IDs for components
            components = crossroad.get("components", [])
            component_ids = []
            for comp in components:
                comp_id = self.indexer.get_or_create_id(comp)
                component_ids.append(comp_id)

            compressed_crossroad: Dict[str, Any] = {
                "id": crossroad.get("id"),
                "c": component_ids,  # components
                "cnt": crossroad.get("integration_count", 0),  # count
            }

            # Add criticality if present
            if "criticality" in crossroad:
                crit = crossroad["criticality"]
                # Map to codes: h=high, m=medium, l=low
                crit_code = {"high": "h", "medium": "m", "low": "l"}.get(crit, "m")
                compressed_crossroad["crit"] = crit_code

            compressed.append(compressed_crossroad)

        return compressed

    def _compress_critical_paths(self, critical_paths: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compress critical paths analysis."""
        compressed = []

        for path in critical_paths:
            entry_point = path.get("entry_point", "")
            entry_id = self.indexer.get_or_create_id(entry_point)

            compressed_path: Dict[str, Any] = {
                "id": path.get("id"),
                "ep": entry_id,  # entry_point
                "cc": path.get("call_count", 0),  # call_count
            }

            # Add complexity if present
            if "complexity" in path:
                cplx = path["complexity"]
                cplx_code = {"high": "h", "medium": "m", "low": "l"}.get(cplx, "m")
                compressed_path["cx"] = cplx_code

            compressed.append(compressed_path)

        return compressed

    def _compress_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Compress metadata section."""
        return abbreviate_keys({
            "total_integration_points": metadata.get("total_integration_points", 0),
            "total_crossroads": metadata.get("total_crossroads", 0),
            "analysis_timestamp": metadata.get("analysis_timestamp", ""),
            "files_analyzed": metadata.get("files_analyzed", 0),
            "components_found": metadata.get("components_found", 0),
        })

    def write(self, output: Dict[str, Any], filepath: str, readable: bool = False) -> None:
        """Write output to file.

        Args:
            output: Formatted output dictionary
            filepath: Output file path
            readable: If True, write pretty-printed JSON (for debugging)
        """
        if readable:
            # Pretty-print for human reading
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
        else:
            # Minified for production (reduces by another ~30%)
            write_compact_json(output, filepath)


def create_compact_formatter() -> CompactFormatter:
    """Factory function to create formatter."""
    return CompactFormatter()
