"""
Integration Mapper - Python AST Code Analysis Tool

A production-ready Python AST analyzer that generates hierarchical JSON maps
showing every connection between Python codebase components.
"""

__version__ = "1.0.0"
__author__ = "Guard8.ai Development Team"
__license__ = "MIT"

from .mapper import IntegrationMapper

__all__ = ["IntegrationMapper"]
