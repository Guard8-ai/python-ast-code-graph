"""
Abbreviation mappings for key and type compression.

Provides mappings for compressing JSON keys and type strings to reduce token usage.
Includes bidirectional functions for abbreviating and expanding keys.

Token Savings:
- key abbreviations: 20% reduction (type→t, name→n, etc.)
- type codes: 30% reduction (function→f, class→c, etc.)
- integration codes: 25% reduction (import→im, call→c, etc.)
"""

from typing import Any, Dict, List, Union


# JSON key abbreviations: long → short
KEY_ABBREV: Dict[str, str] = {
    # Common keys
    "type": "t",
    "name": "n",
    "parent": "p",
    "children": "ch",
    "id": "id",

    # Component attributes
    "fqn": "fqn",
    "line_range": "lr",
    "line": "l",
    "docstring": "doc",
    "path": "path",

    # Edge attributes
    "source": "s",
    "target": "tg",
    "args": "a",
    "returns": "ret",
    "calls": "c",
    "called_by": "cb",

    # Metadata
    "metadata": "meta",
    "timestamp": "ts",
    "files_analyzed": "fa",
    "components_found": "cf",
    "total_integration_points": "tip",
    "total_crossroads": "tcr",
    "analysis_timestamp": "ats",

    # Index and structure
    "idx": "idx",
    "codebase_tree": "ct",
    "global_integration_map": "gim",
    "crossroads": "cr",
    "critical_paths": "cp",
    "integration_count": "ic",
    "criticality": "crit",
    "entry_point": "ep",
    "call_count": "cc",
    "components": "c",
    "edges": "e",
    "statistics": "stats",
    "version": "v",
}

# Component type codes: long string → short code
TYPE_CODES: Dict[str, str] = {
    "package": "pk",
    "module": "mo",
    "class": "c",
    "function": "f",
    "method": "m",
    "attribute": "a",
}

# Integration edge type codes: long string → short code
INTEGRATION_CODES: Dict[str, str] = {
    "import": "im",
    "call": "c",
    "inherit": "in",
    "attribute_read": "ar",
    "attribute_write": "aw",
    "decorator": "d",
}

# Reverse mappings for decoding
REVERSE_KEY_ABBREV: Dict[str, str] = {v: k for k, v in KEY_ABBREV.items()}
REVERSE_TYPE_CODES: Dict[str, str] = {v: k for k, v in TYPE_CODES.items()}
REVERSE_INTEGRATION_CODES: Dict[str, str] = {v: k for k, v in INTEGRATION_CODES.items()}


def abbreviate_keys(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """Recursively abbreviate dictionary keys.

    Args:
        data: Data structure (dict, list, or scalar) to abbreviate

    Returns:
        Data with all dictionary keys abbreviated using KEY_ABBREV mapping

    Example:
        >>> data = {"type": "function", "name": "save"}
        >>> abbrev = abbreviate_keys(data)
        >>> print(abbrev)
        {"t": "function", "n": "save"}
    """
    if isinstance(data, dict):
        return {
            KEY_ABBREV.get(k, k): abbreviate_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [abbreviate_keys(item) for item in data]
    return data


def expand_keys(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """Recursively expand abbreviated dictionary keys.

    Reverse operation of abbreviate_keys(). Restores abbreviated keys to full names.

    Args:
        data: Data structure with abbreviated keys to expand

    Returns:
        Data with all abbreviated dictionary keys expanded

    Example:
        >>> data = {"t": "function", "n": "save"}
        >>> expanded = expand_keys(data)
        >>> print(expanded)
        {"type": "function", "name": "save"}
    """
    if isinstance(data, dict):
        return {
            REVERSE_KEY_ABBREV.get(k, k): expand_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [expand_keys(item) for item in data]
    return data


def abbreviate_type_code(type_str: str) -> str:
    """Convert component type string to code.

    Args:
        type_str: Type string (e.g., "function")

    Returns:
        Abbreviated type code (e.g., "f")

    Example:
        >>> abbreviate_type_code("function")
        "f"
        >>> abbreviate_type_code("class")
        "c"
    """
    return TYPE_CODES.get(type_str, type_str)


def expand_type_code(code: str) -> str:
    """Convert type code back to full string.

    Args:
        code: Type code (e.g., "f")

    Returns:
        Full type string (e.g., "function")

    Example:
        >>> expand_type_code("f")
        "function"
    """
    return REVERSE_TYPE_CODES.get(code, code)


def abbreviate_integration_code(integration_type: str) -> str:
    """Convert integration type string to code.

    Args:
        integration_type: Integration type (e.g., "call")

    Returns:
        Abbreviated integration code (e.g., "c")

    Example:
        >>> abbreviate_integration_code("call")
        "c"
        >>> abbreviate_integration_code("import")
        "im"
    """
    return INTEGRATION_CODES.get(integration_type, integration_type)


def expand_integration_code(code: str) -> str:
    """Convert integration code back to full string.

    Args:
        code: Integration code (e.g., "c")

    Returns:
        Full integration type string (e.g., "call")

    Example:
        >>> expand_integration_code("c")
        "call"
    """
    return REVERSE_INTEGRATION_CODES.get(code, code)
