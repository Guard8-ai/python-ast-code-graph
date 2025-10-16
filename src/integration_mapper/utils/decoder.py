"""
CompactDecoder: Reverses CompactFormatter compression for analysis.

This module provides utilities to decode compact format maps back to verbose
format for full analysis. It enables round-trip transformation:
compact → decode → verbose (lossless)

Key capabilities:
- Expand IDs back to FQNs using index
- Restore abbreviated keys to full names
- Convert edge arrays back to objects
- Reconstruct full component hierarchy

Example:
    >>> from decoder import CompactDecoder
    >>> from compact_formatter import CompactFormatter
    >>>
    >>> # Encode
    >>> formatter = CompactFormatter()
    >>> compact_map = formatter.build_output(symbol_table, edges, metadata)
    >>>
    >>> # Decode
    >>> decoder = CompactDecoder()
    >>> decoded_map = decoder.decode(compact_map)
    >>> # decoded_map is equivalent to verbose format output
"""

from typing import Dict, Any, List, Optional


class CompactDecoder:
    """Reverses CompactFormatter compression for round-trip analysis.

    This decoder takes compact format output and expands it back to verbose
    format, enabling full analysis on compact maps. All information is preserved
    in the round-trip: verbose → compact → verbose.

    The decoder handles:
    1. **ID Expansion**: Replace integer IDs with FQNs from index
    2. **Key Expansion**: Restore abbreviated keys to full names
    3. **Edge Expansion**: Convert compact arrays to full edge objects
    4. **Hierarchy Reconstruction**: Rebuild component relationships

    Attributes:
        None (stateless)

    Methods:
        decode: Main entry point for decoding
        decode_metadata: Expand abbreviated metadata
        decode_components: Expand compact component list
        decode_edges: Expand compact edge arrays
    """

    # Key abbreviation mappings (reverse of abbreviations.py)
    KEY_EXPANSION = {
        "i": "id",
        "n": "name",
        "t": "type",
        "f": "fqn",
        "p": "parent_id",
        "l": "line_range",
        "d": "docstring",
        "c": "children",
        "m": "methods",
    }

    # Type code expansions (reverse of abbreviations.TYPE_CODES)
    TYPE_EXPANSION = {
        "mod": "module",
        "pkg": "package",
        "cls": "class",
        "fn": "function",
        "mth": "method",
        "var": "variable",
        "imp": "import",
    }

    # Integration code expansions (reverse of abbreviations.INTEGRATION_CODES)
    EDGE_TYPE_EXPANSION = {
        "imp": "import",
        "cal": "call",
        "attr": "attribute",
        "inh": "inheritance",
        "imp_mod": "import_module",
        "imp_frm": "import_from",
        "fn_cal": "function_call",
        "attr_acc": "attribute_access",
    }

    # Metadata abbreviation expansions
    METADATA_EXPANSION = {
        "tip": "total_integration_points",
        "crs": "total_crossroads",
        "ts": "analysis_timestamp",
        "fa": "files_analyzed",
        "cf": "components_found",
    }

    def decode(self, compact_map: Dict[str, Any]) -> Dict[str, Any]:
        """Decode compact format to verbose format.

        Main entry point that orchestrates the decoding process:
        1. Extracts FQN index from compact map
        2. Expands metadata
        3. Expands components
        4. Expands edges
        5. Rebuilds complete verbose structure

        Args:
            compact_map: Compact format dict from CompactFormatter with keys:
                - idx: FQN Index mapping string IDs to FQNs
                - md: Abbreviated metadata
                - cmp: Flat list of compact components
                - edg: Compact edge arrays
                - crd: Crossroads (optional)
                - cp: Critical paths (optional)

        Returns:
            Verbose format dict equivalent to VerboseFormatter output:
            {
                "metadata": {...},
                "codebase_tree": {...},
                "global_integration_map": {...},
                "integration_edges": [...]
            }

        Note:
            Round-trip transformation is lossless for all information
            except formatting (whitespace, key order, etc.).
        """
        # Extract components from compact map
        fqn_index = compact_map.get("idx", {})
        compact_metadata = compact_map.get("md", {})
        compact_components = compact_map.get("cmp", [])
        compact_edges = compact_map.get("edg", [])
        crossroads = compact_map.get("crd", [])
        critical_paths = compact_map.get("cp", [])

        # Decode each section
        metadata = self._decode_metadata(compact_metadata)
        components = self._decode_components(compact_components, fqn_index)
        edges = self._decode_edges(compact_edges, fqn_index)
        tree = self._rebuild_tree(components)

        # Assemble verbose output
        return {
            "metadata": metadata,
            "codebase_tree": tree,
            "global_integration_map": {
                "crossroads": crossroads,
                "critical_paths": critical_paths,
                "data_flows": [],
                "statistics": {
                    "total_components": len(components),
                    "total_integration_points": len(edges),
                    "total_edges": len(edges)
                }
            },
            "integration_edges": edges
        }

    def _decode_metadata(self, compact_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Expand abbreviated metadata to verbose form.

        Args:
            compact_metadata: Dict with abbreviated keys (tip, crs, ts, fa, cf)

        Returns:
            Dict with full metadata key names
        """
        return {
            self.METADATA_EXPANSION.get(k, k): v
            for k, v in compact_metadata.items()
        }

    def _decode_components(self, compact_components: List[Dict[str, Any]],
                          fqn_index: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        """Expand compact components to verbose form.

        Converts flat list of compact components back to full component objects
        with expanded keys and ID→FQN references.

        Args:
            compact_components: List of compact component dicts with abbreviated keys
            fqn_index: Dict mapping string IDs to FQN strings

        Returns:
            Dict mapping FQN strings to expanded component dicts
        """
        expanded_components: Dict[str, Dict[str, Any]] = {}

        for comp in compact_components:
            # Extract ID and expand to FQN
            component_id = comp.get("i")
            fqn = fqn_index.get(str(component_id), f"<unknown:{component_id}>")

            # Build expanded component
            expanded = {
                "fqn": fqn,
                "name": comp.get("n", ""),
                "type": self._expand_type_code(comp.get("t", "")),
                "line_range": comp.get("l", []),
            }

            # Add optional fields
            if "d" in comp:
                expanded["docstring"] = comp["d"]

            # Expand children IDs to FQNs
            if "c" in comp:
                expanded["children"] = {
                    fqn_index.get(str(child_id), f"<unknown:{child_id}>"): fqn_index.get(str(child_id), f"<unknown:{child_id}>")
                    for child_id in comp["c"]
                }

            # Expand methods IDs to FQNs
            if "m" in comp:
                expanded["methods"] = {
                    fqn_index.get(str(method_id), f"<unknown:{method_id}>").split(".")[-1]: fqn_index.get(str(method_id), f"<unknown:{method_id}>")
                    for method_id in comp["m"]
                }

            expanded_components[fqn] = expanded

        return expanded_components

    def _decode_edges(self, compact_edges: List[List[Any]],
                     fqn_index: Dict[str, str]) -> List[Dict[str, Any]]:
        """Expand compact edge arrays to verbose edge objects.

        Converts compact edge arrays [src_id, tgt_id, type, line, ?target_fqn]
        to full edge objects with all metadata.

        Args:
            compact_edges: List of compact edge arrays
            fqn_index: Dict mapping string IDs to FQN strings

        Returns:
            List of expanded edge dicts
        """
        expanded_edges: List[Dict[str, Any]] = []

        for edge in compact_edges:
            if len(edge) < 4:
                continue  # Invalid edge

            source_id = edge[0]
            target_id = edge[1]
            type_code = edge[2]
            line = edge[3]

            # Resolve IDs to FQNs
            source_fqn = fqn_index.get(str(source_id), f"<unknown:{source_id}>")

            # For target: check if it's external (target_id == -1)
            if target_id == -1 and len(edge) > 4:
                # External module - FQN is in edge[4]
                target_fqn = edge[4]
            else:
                target_fqn = fqn_index.get(str(target_id), f"<unknown:{target_id}>")

            # Build expanded edge
            expanded_edge = {
                "type": self._expand_edge_type(type_code),
                "source": source_fqn,
                "target": target_fqn,
                "line": line,
                "integration_type": self._expand_edge_type(type_code),
            }

            expanded_edges.append(expanded_edge)

        return expanded_edges

    def _rebuild_tree(self, components: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild hierarchical tree from flat component dict.

        Reconstructs the hierarchical structure from the flat component
        dictionary using FQN dot-notation paths.

        Args:
            components: Dict mapping FQN strings to component dicts

        Returns:
            Hierarchical tree dict suitable for JSON output
        """
        tree: Dict[str, Any] = {}

        for fqn, component in components.items():
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

            # Add component at leaf
            current[parts[-1]] = component

        return tree

    def _expand_type_code(self, code: str) -> str:
        """Expand abbreviated type code to full name.

        Args:
            code: Abbreviated type code (e.g., "cls", "fn")

        Returns:
            Full type name (e.g., "class", "function")
        """
        return self.TYPE_EXPANSION.get(code, code)

    def _expand_edge_type(self, code: str) -> str:
        """Expand abbreviated edge type code to full name.

        Args:
            code: Abbreviated edge type (e.g., "cal", "imp")

        Returns:
            Full edge type name (e.g., "call", "import")
        """
        return self.EDGE_TYPE_EXPANSION.get(code, code)
