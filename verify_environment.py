#!/usr/bin/env python3
"""
Environment verification script for Integration Mapper project.

Verifies:
- Python 3.8+ available
- All required stdlib modules present
- Basic AST parsing works
"""

import sys
import ast
import json
import argparse
import pathlib


def verify_python_version():
    """Verify Python 3.8+ is available."""
    if sys.version_info < (3, 8):
        raise RuntimeError(f"Python 3.8+ required, got {sys.version_info.major}.{sys.version_info.minor}")
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}+ available")


def verify_stdlib_modules():
    """Verify all required stdlib modules are available."""
    required_modules = ['ast', 'json', 'argparse', 'pathlib']

    for module_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ stdlib.{module_name} available")
        except ImportError as e:
            raise RuntimeError(f"Missing stdlib module: {module_name}") from e


def verify_ast_parsing():
    """Test basic AST parsing functionality."""
    test_code = """
def example_function(x, y):
    '''Example docstring.'''
    return x + y

class ExampleClass:
    def __init__(self):
        self.value = 42
"""

    try:
        tree = ast.parse(test_code)
        assert len(tree.body) == 2, "Expected 2 top-level statements"
        assert isinstance(tree.body[0], ast.FunctionDef), "First statement should be FunctionDef"
        assert isinstance(tree.body[1], ast.ClassDef), "Second statement should be ClassDef"
        print(f"✅ AST parsing works (parsed {len(tree.body)} statements)")
    except Exception as e:
        raise RuntimeError(f"AST parsing failed: {e}") from e


def main():
    """Run all verification checks."""
    print("🔍 INTEGRATION MAPPER: ENVIRONMENT VERIFICATION")
    print("=" * 60)

    try:
        verify_python_version()
        verify_stdlib_modules()
        verify_ast_parsing()

        print("=" * 60)
        print("✅ ALL ENVIRONMENT CHECKS PASSED")
        print("Ready for Integration Mapper development!\n")
        return 0

    except Exception as e:
        print("=" * 60)
        print(f"❌ ENVIRONMENT CHECK FAILED: {e}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
