"""Key and type abbreviations for token-efficient compression.

Maps verbose keys and types to short abbreviations:
- KEY_ABBREV: Long keys → 1-3 character abbreviations (20% reduction)
- TYPE_CODES: Type strings → 1-2 character codes (30% reduction)
- INTEGRATION_CODES: Integration types → codes (10% reduction)
"""

from typing import Any, Dict


# Core structure abbreviations
KEY_ABBREV: Dict[str, str] = {
    # Component metadata
    "type": "t",
    "name": "n",
    "parent": "p",
    "children": "ch",
    "line_range": "lr",
    "line": "l",
    "docstring": "doc",
    "file_id": "fid",
    "fqn": "f",

    # Integration and edges
    "source": "s",
    "target": "tg",  # "t" is taken by "type"
    "args": "a",
    "returns": "ret",
    "calls": "c",
    "called_by": "cb",
    "reads": "rd",
    "writes": "wr",
    "imports": "im",
    "imported_by": "imb",
    "inherits": "inh",
    "inherited_by": "inhb",

    # Metadata
    "file": "f",
    "path": "pth",
    "integration_points": "ip",
    "usage_count": "uc",
    "confidence": "conf",
    "timestamp": "ts",
    "stats": "st",
    "count": "c",
    "relationships": "r",
    "index": "idx",
    "components": "cmp",
    "edges": "e",
    "crossroads": "crd",
    "critical_paths": "cp",
    "version": "v",
    "metadata": "meta",
}

# Component type abbreviations (2 chars for clarity)
TYPE_CODES: Dict[str, str] = {
    "package": "pk",
    "module": "mo",
    "class": "cl",
    "function": "fn",
    "method": "mt",
    "attribute": "at",
    "variable": "va",
}

# Integration type abbreviations
INTEGRATION_CODES: Dict[str, str] = {
    "import": "im",
    "call": "cl",
    "inherit": "ih",
    "attribute_read": "ar",
    "attribute_write": "aw",
    "decorator": "dc",
    "type_hint": "th",
    "exception": "ex",
}


def abbreviate_keys(data: Any) -> Any:
    """Recursively abbreviate dictionary keys in data structure.

    Converts all verbose keys to abbreviations while preserving values.
    Handles nested dicts and lists recursively.

    Args:
        data: Dictionary, list, or primitive value to abbreviate

    Returns:
        Data structure with abbreviated keys

    Example:
        >>> orig = {"type": "method", "name": "save", "line_range": [42, 56]}
        >>> abbr = abbreviate_keys(orig)
        >>> assert abbr == {"t": "method", "n": "save", "lr": [42, 56]}

    Token savings: Reduces key name length from average 15 chars to 3 chars.
    """
    if isinstance(data, dict):
        return {
            KEY_ABBREV.get(k, k): abbreviate_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [abbreviate_keys(item) for item in data]
    return data


def expand_keys(data: Any) -> Any:
    """Reverse abbreviation - expand abbreviated keys back to verbose form.

    Converts all abbreviated keys back to full names for human readability.
    Used by decoder utility to expand compact format to verbose format.

    Args:
        data: Dictionary, list, or primitive value to expand

    Returns:
        Data structure with expanded keys

    Example:
        >>> abbr = {"t": "method", "n": "save", "lr": [42, 56]}
        >>> expanded = expand_keys(abbr)
        >>> assert expanded == {"type": "method", "name": "save", "line_range": [42, 56]}
    """
    # Create reverse mapping: abbrev → full
    reverse_abbrev = {v: k for k, v in KEY_ABBREV.items()}

    if isinstance(data, dict):
        return {
            reverse_abbrev.get(k, k): expand_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [expand_keys(item) for item in data]
    return data


def abbreviate_type(type_str: str) -> str:
    """Convert component type to abbreviation."""
    return TYPE_CODES.get(type_str, type_str)


def expand_type(type_abbr: str) -> str:
    """Convert type abbreviation back to full name."""
    reverse_types = {v: k for k, v in TYPE_CODES.items()}
    return reverse_types.get(type_abbr, type_abbr)


def abbreviate_integration(integration_str: str) -> str:
    """Convert integration type to abbreviation."""
    return INTEGRATION_CODES.get(integration_str, integration_str)


def expand_integration(integration_abbr: str) -> str:
    """Convert integration abbreviation back to full name."""
    reverse_integrations = {v: k for k, v in INTEGRATION_CODES.items()}
    return reverse_integrations.get(integration_abbr, integration_abbr)


def get_abbreviation_stats() -> Dict[str, int]:
    """Get statistics about abbreviation effectiveness."""
    # Calculate average character savings
    total_abbr_chars = sum(len(v) for v in KEY_ABBREV.values())
    total_full_chars = sum(len(k) for k in KEY_ABBREV.keys())
    total_type_chars = sum(len(v) for v in TYPE_CODES.values())
    total_type_full = sum(len(k) for k in TYPE_CODES.keys())

    return {
        "keys": {
            "count": len(KEY_ABBREV),
            "full_chars": total_full_chars,
            "abbr_chars": total_abbr_chars,
            "avg_savings_pct": int((1 - total_abbr_chars / total_full_chars) * 100)
        },
        "types": {
            "count": len(TYPE_CODES),
            "full_chars": total_type_full,
            "abbr_chars": total_type_chars,
            "avg_savings_pct": int((1 - total_type_chars / total_type_full) * 100)
        }
    }
