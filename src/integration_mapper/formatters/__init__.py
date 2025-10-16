"""
Formatters package: Pluggable output formatters for integration maps.

This package provides different output formats for integration maps:
- VerboseFormatter: Default format with full details (maintains backward compatibility)
- CompactFormatter: Compressed format for context-aware AI usage (85%+ token reduction)

Each formatter implements the BaseFormatter interface, enabling easy switching
between formats based on use case.
"""

from .base_formatter import BaseFormatter
from .verbose_formatter import VerboseFormatter

__all__ = ["BaseFormatter", "VerboseFormatter"]
