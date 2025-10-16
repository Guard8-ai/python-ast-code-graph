"""Output formatters for integration mapper.

Provides pluggable formatters for different output modes:
- VerboseFormatter: Original hierarchical format (default)
- CompactFormatter: Context-aware token-efficient format
"""

from .verbose_formatter import VerboseFormatter, create_verbose_formatter
from .compact_formatter import CompactFormatter, create_compact_formatter

__all__ = [
    "VerboseFormatter",
    "CompactFormatter",
    "create_verbose_formatter",
    "create_compact_formatter",
]
