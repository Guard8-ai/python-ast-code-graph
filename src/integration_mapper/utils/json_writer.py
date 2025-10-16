"""Utilities for writing minified and readable JSON output.

Provides functions for writing JSON in both compact (minified) and readable
(pretty-printed) formats for different use cases.
"""

import json
from typing import Any, Dict
from pathlib import Path


def write_compact_json(data: Dict[str, Any], filepath: str) -> None:
    """Write JSON in compact minified format (no whitespace).

    Minified output reduces file size by ~30% compared to pretty-printed JSON.
    This is the primary format for token-efficient compressed maps.

    Args:
        data: Dictionary to write
        filepath: Output file path

    Example:
        >>> data = {"v": "2.0", "idx": {"1": "myapp"}}
        >>> write_compact_json(data, "map_compact.json")
        # Output: {"v":"2.0","idx":{"1":"myapp"}}
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            separators=(',', ':'),  # No spaces after separators
            ensure_ascii=False,  # Allow unicode characters
            sort_keys=False
        )


def write_readable_json(data: Dict[str, Any], filepath: str) -> None:
    """Write JSON in pretty-printed readable format.

    Pretty-printed format is easier for humans to read and debug,
    but uses ~40% more space. Used for documentation and debugging.

    Args:
        data: Dictionary to write
        filepath: Output file path

    Example:
        >>> data = {"v": "2.0", "idx": {"1": "myapp"}}
        >>> write_readable_json(data, "map_readable.json")
        # Output:
        # {
        #   "v": "2.0",
        #   "idx": {
        #     "1": "myapp"
        #   }
        # }
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
            sort_keys=False
        )


def estimate_token_count(filepath: str) -> int:
    """Estimate token count of JSON file using rough approximation.

    Uses: file_size_bytes / 4 ≈ tokens
    This is a rough estimate. For accurate counts, use GPT tokenizer.

    Args:
        filepath: Path to JSON file

    Returns:
        Estimated token count

    Example:
        >>> tokens = estimate_token_count("map_compact.json")
        >>> print(f"Estimated tokens: {tokens:,}")
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    file_size = path.stat().st_size
    # Rough estimate: ~4 bytes per token for JSON (conservative)
    return max(1, file_size // 4)


def get_file_size_info(filepath: str) -> Dict[str, Any]:
    """Get detailed file size information.

    Args:
        filepath: Path to file

    Returns:
        Dictionary with size stats in bytes, KB, and MB

    Example:
        >>> info = get_file_size_info("map_compact.json")
        >>> print(f"Size: {info['kb']:.1f} KB")
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    size_bytes = path.stat().st_size
    return {
        "bytes": size_bytes,
        "kb": size_bytes / 1024,
        "mb": size_bytes / (1024 ** 2),
        "estimated_tokens": max(1, size_bytes // 4),
    }
