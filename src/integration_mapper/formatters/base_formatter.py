"""
BaseFormatter: Abstract base class for pluggable output formatters.

This module defines the abstract interface that all output formatters must implement.
It enables switching between different output formats (verbose, compact, etc.) through
a consistent API.

Formatters handle three core responsibilities:
1. format_components(): Transform component hierarchy into format-specific structure
2. format_edges(): Transform integration edges into format-specific structure
3. build_output(): Combine formatted components and edges into final output

Example:
    >>> from base_formatter import BaseFormatter
    >>> from verbose_formatter import VerboseFormatter
    >>>
    >>> symbol_table = {...}  # Component data
    >>> edges = [...]          # Integration edges
    >>>
    >>> formatter = VerboseFormatter()
    >>> output = formatter.build_output(symbol_table, edges, {})
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseFormatter(ABC):
    """Abstract base class for integration map formatters.

    Formatters are responsible for converting analyzed code structure and integration
    edges into various output formats (verbose JSON, compact, etc.). Each formatter
    must implement the three core methods defined here.

    The formatter receives:
    - symbol_table: Dict mapping FQN strings to component metadata
    - integration_edges: List of edge dicts representing connections
    - metadata: Dict with analysis statistics (timestamp, file count, etc.)

    Each formatter is responsible for:
    1. Organizing component data appropriately for its format
    2. Representing edges according to format conventions
    3. Producing complete, valid output structure

    Attributes:
        None at base level (subclasses may add format-specific state)

    Methods:
        format_components: Transform component hierarchy
        format_edges: Transform integration edges
        build_output: Produce final output structure
    """

    @abstractmethod
    def format_components(self, symbol_table: Dict[str, Dict[str, Any]]) -> Any:
        """Format components/hierarchy for output.

        Transforms the symbol table (component metadata) into the format-specific
        representation. This could be:
        - Verbose: Full hierarchical tree with all metadata
        - Compact: Flat list with ID references
        - Other: Format-specific structure

        Args:
            symbol_table: Dictionary mapping FQN strings to component metadata.
                Each component contains:
                - type: Component type (module, class, function, etc.)
                - fqn: Fully qualified name
                - name: Local name
                - line_range: [start_line, end_line]
                - path: File path relative to root
                - docstring: Component docstring (may be None)
                - children: Dict of child components
                - imports: List of import statements (for modules)

        Returns:
            Format-specific representation of components. Type depends on formatter:
            - VerboseFormatter: Dict with tree structure
            - CompactFormatter: List with flat component objects
            - Other: Implementation-dependent

        Note:
            The symbol_table keys are FQNs (fully qualified names).
            Root-level components have no package prefix.
        """
        pass

    @abstractmethod
    def format_edges(self, edges: List[Dict[str, Any]]) -> Any:
        """Format integration edges for output.

        Transforms the list of integration edges (connections between components)
        into the format-specific representation. This could be:
        - Verbose: Full edge objects with all details
        - Compact: Array tuples with minimal data
        - Other: Format-specific structure

        Args:
            edges: List of edge dictionaries. Each edge contains:
                - type: Edge type (import, call, attribute, inheritance)
                - source: FQN of source component
                - target: FQN of target component (or external module)
                - line: Line number where edge occurs
                - integration_type: More specific type (e.g., import_module, function_call)
                - Additional fields depending on edge type (items, args, access, etc.)

        Returns:
            Format-specific representation of edges. Type depends on formatter:
            - VerboseFormatter: List of full edge dicts
            - CompactFormatter: List of compact edge arrays [src_id, tgt_id, type, line]
            - Other: Implementation-dependent

        Note:
            Some formatters may deduplicate edges or filter by type.
        """
        pass

    @abstractmethod
    def build_output(self, symbol_table: Dict[str, Dict[str, Any]],
                     edges: List[Dict[str, Any]],
                     metadata: Dict[str, Any],
                     crossroads: List[Dict[str, Any]] = None,
                     critical_paths: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build final output structure.

        Combines formatted components, edges, metadata, and analysis results into
        a complete output dictionary ready for serialization (JSON, etc.).

        This method orchestrates the formatting process:
        1. Calls format_components() to transform component hierarchy
        2. Calls format_edges() to transform integration edges
        3. Assembles all parts into final output structure
        4. Includes metadata, crossroads, and critical paths

        Args:
            symbol_table: Dictionary mapping FQN strings to component metadata
            edges: List of integration edge dictionaries
            metadata: Dictionary with analysis metadata:
                - total_integration_points: Count of edges
                - total_crossroads: Count of identified crossroads
                - analysis_timestamp: ISO format timestamp
                - files_analyzed: Number of files analyzed
                - components_found: Number of components found
            crossroads: List of crossroad analysis results (may be None)
            critical_paths: List of critical path analysis results (may be None)

        Returns:
            Complete output structure as Dict[str, Any]. Format depends on formatter:
            - VerboseFormatter: Full hierarchical JSON with all details
            - CompactFormatter: Minified JSON with compression
            - Other: Implementation-dependent

        The output must include:
        - metadata: Analysis metadata
        - components/codebase_tree: Formatted component hierarchy
        - edges/global_integration_map: Formatted edges and analysis results
        - Format-specific optimizations (compression, abbreviations, etc.)

        Note:
            The concrete implementation is responsible for deciding how to structure
            the output and what to include/exclude for that format.
        """
        pass

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate output structure (optional).

        Override in subclasses to add format-specific validation.

        Args:
            output: Output dictionary to validate

        Returns:
            True if output is valid, False otherwise

        Default:
            Returns True (no validation by default)
        """
        return True
