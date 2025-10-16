"""VerboseFormatter: Original hierarchical output format.

Produces the default hierarchical JSON output with full component
tree and integration details. This is the original format, kept
for backward compatibility.
"""

import json
from typing import Any, Dict
from pathlib import Path


class VerboseFormatter:
    """Original verbose formatter (default, backward compatible).

    Output structure matches the hierarchical tree structure directly.
    This is the original integration_mapper.py output format.
    """

    def format_output(self, verbose_output: Dict[str, Any]) -> Dict[str, Any]:
        """Return output as-is (no compression).

        For verbose mode, we just return the original output structure
        without any modifications.

        Args:
            verbose_output: Original output from mapper.run()

        Returns:
            Same structure (no compression)
        """
        return verbose_output

    def write(self, output: Dict[str, Any], filepath: str, readable: bool = True) -> None:
        """Write output to file with pretty-printing.

        Args:
            output: Output dictionary
            filepath: Output file path
            readable: Always True for verbose mode (pretty-printed by default)
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)


def create_verbose_formatter() -> VerboseFormatter:
    """Factory function to create verbose formatter."""
    return VerboseFormatter()
