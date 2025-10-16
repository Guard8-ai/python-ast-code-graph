"""Compression and utility modules for token-efficient output."""

from .indexer import ComponentIndexer
from .abbreviations import (
    abbreviate_keys,
    expand_keys,
    abbreviate_type,
    expand_type,
    abbreviate_integration,
    expand_integration,
    KEY_ABBREV,
    TYPE_CODES,
    INTEGRATION_CODES,
)
from .json_writer import (
    write_compact_json,
    write_readable_json,
    estimate_token_count,
    get_file_size_info,
)

__all__ = [
    # Indexer
    "ComponentIndexer",
    # Abbreviations
    "abbreviate_keys",
    "expand_keys",
    "abbreviate_type",
    "expand_type",
    "abbreviate_integration",
    "expand_integration",
    "KEY_ABBREV",
    "TYPE_CODES",
    "INTEGRATION_CODES",
    # JSON writer
    "write_compact_json",
    "write_readable_json",
    "estimate_token_count",
    "get_file_size_info",
]
