# Integration Mapper

**Production-ready Python AST analyzer with hierarchical integration mapping**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: industry](https://img.shields.io/badge/code%20style-industry-brightgreen.svg)](https://github.com/Guard8-ai/python-ast-code-graph)

Integration Mapper generates hierarchical JSON maps showing **every connection** between Python codebase components. Unlike traditional static analysis tools, it provides a complete, navigable view of your entire project's structure and interconnections.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Guard8-ai/python-ast-code-graph.git
cd python-ast-code-graph

# Run analysis on your Python project
python src/integration_mapper/mapper.py --root /path/to/your/project --output analysis.json

# Verify the output
python -m json.tool analysis.json | head -50
```

---

## ✨ Features

- **📊 Hierarchical Component Discovery** - Complete tree of modules, classes, functions, and methods
- **🔗 Rich Integration Mapping** - Captures imports, calls, attributes, and inheritance
- **🌊 Flow Analysis** - Identifies module boundaries, crossroads, and critical paths
- **⚡ Zero Dependencies** - Uses only Python standard library
- **🎯 Deterministic FQN System** - Unique identifiers for reliable component lookup
- **📦 Production-Ready Output** - Valid JSON schema for programmatic consumption

---

## 📖 Documentation

- **[Quick Start Guide](docs/DEVELOPER_QUICKSTART.md)** - Get up and running in 5 minutes
- **[Complete Wiki](docs/WIKI.md)** - Comprehensive 2600+ line reference guide
- **[CLI Usage](docs/CLI_USAGE.md)** - Command-line interface documentation
- **[Implementation Guide](docs/IMPLEMENTATION.md)** - Architecture and design decisions
- **[JSON Schema](docs/json_schema_design.md)** - Output format specification

---

## 🎯 Use Cases

### Code Refactoring
Understand impact analysis before making changes:
```bash
python src/integration_mapper/mapper.py --root /path/to/django_project --output analysis.json
# Query integrations to find all callers of a specific function
# Identify module boundaries for safe decoupling
```

### Technical Debt Assessment
Measure codebase complexity and coupling:
- Count total components and integrations
- Identify highly coupled modules (crossroads)
- Track metrics over time

### Code Review & Onboarding
Help new developers understand architecture:
- Generate hierarchical maps showing all components
- Visualize integration points and data flow
- Navigate using FQNs to important components

---

## 📊 Example Output

```json
{
  "metadata": {
    "total_components": 1247,
    "total_integrations": 3891,
    "hierarchy_depth": 6,
    "analysis_complete": true
  },
  "hierarchy": {
    "my_project": {
      "type": "module",
      "fqn": "my_project",
      "children": { ... }
    }
  },
  "integrations": [ ... ],
  "flow": {
    "module_boundaries": [ ... ],
    "critical_paths": [ ... ]
  }
}
```

See [examples/](examples/) for complete analysis outputs.

---

## 🏗️ Architecture

Integration Mapper uses a **three-phase pipeline architecture**:

```
Phase 1: Hierarchy Building
    ↓
Phase 2: Integration Extraction
    ↓
Phase 3: Flow Analysis
    ↓
JSON Output
```

Each phase is independent and modular, implemented as a separate AST visitor class.

**Learn more:** [Implementation Guide](docs/IMPLEMENTATION.md)

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/test_integration_mapper.py -v

# Run with coverage
python -m pytest tests/test_integration_mapper.py --cov=src/integration_mapper

# All 8 tests pass with 100% pass rate
```

---

## 📋 Requirements

- Python 3.8 or higher
- No external dependencies (uses stdlib only)

Verify your environment:
```bash
python scripts/verify_environment.py
```

---

## 🛠️ Command Line Options

```bash
python src/integration_mapper/mapper.py [OPTIONS]

Options:
  --root PATH          Project root directory (mutually exclusive with --file)
  --file PATH          Single Python file to analyze (mutually exclusive with --root)
  --output PATH        Output JSON file path (default: integration_map.json)
  --exclude PATTERNS   Glob patterns to exclude (can be specified multiple times)
  --verbose           Show detailed progress messages
```

**Examples:**
```bash
# Analyze entire directory
python src/integration_mapper/mapper.py \
  --root /path/to/project \
  --output analysis.json \
  --exclude "*/tests/*" --exclude "*/migrations/*" \
  --verbose

# Analyze single file
python src/integration_mapper/mapper.py \
  --file src/integration_mapper/mapper.py \
  --output single_file_analysis.json
```

---

## 📁 Project Structure

```
python-ast-code-graph/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── src/                               # Source code
│   └── integration_mapper/
│       ├── __init__.py               # Package initialization
│       └── mapper.py                 # Main analysis engine
├── tests/                            # Test suite
│   └── test_integration_mapper.py   # Comprehensive tests (8 tests)
├── docs/                             # Documentation
│   ├── WIKI.md                      # Complete reference (2600+ lines)
│   ├── DEVELOPER_QUICKSTART.md      # Quick start guide
│   ├── CLI_USAGE.md                 # CLI documentation
│   ├── IMPLEMENTATION.md            # Architecture guide
│   └── json_schema_design.md        # Schema specification
├── examples/                         # Example outputs
│   └── integration_map.json         # Sample analysis output
├── scripts/                          # Utility scripts
│   ├── validate_schema.py           # Schema validation
│   └── verify_environment.py        # Environment checker
└── tasks/                            # TaskGuard task management
    └── ...                           # Task tracking files
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/WIKI.md#8-contributing-guidelines) for:

- Code style standards
- Testing requirements
- Pull request process
- Development workflow

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with Python's powerful `ast` module
- Designed for integration with Guard8.ai security analysis platform
- Follows industry-standard Python project structure

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Guard8-ai/python-ast-code-graph/issues)
- **Documentation:** [Complete Wiki](docs/WIKI.md)
- **Examples:** [Example Outputs](examples/)

---

**Made with ❤️ by Guard8.ai Development Team**
