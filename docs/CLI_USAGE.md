# Integration Mapper: CLI Usage Guide

## Command Line Interface

The Integration Mapper provides a comprehensive CLI for analyzing Python codebases.

### Basic Usage

```bash
python integration_mapper.py --root /path/to/project --output map.json
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--root` | ✅ YES | N/A | Root directory of codebase to analyze |
| `--output` | ❌ NO | `integration_map.json` | Output JSON file path |
| `--exclude` | ❌ NO | N/A | Glob pattern to exclude files (repeatable) |
| `--verbose` | ❌ NO | False | Show progress output during analysis |
| `-h, --help` | ❌ NO | N/A | Show help message |

### Examples

#### Analyze current directory
```bash
python integration_mapper.py --root .
```

#### Specify custom output file
```bash
python integration_mapper.py --root ./myproject --output architecture.json
```

#### Exclude test and migration files
```bash
python integration_mapper.py \
  --root ./myproject \
  --output map.json \
  --exclude "*/tests/*" \
  --exclude "*/migrations/*" \
  --exclude "*/__pycache__/*"
```

#### Verbose output with custom settings
```bash
python integration_mapper.py \
  --root /var/www/django_app \
  --output full_map.json \
  --exclude "*/venv/*" \
  --exclude "*/node_modules/*" \
  --verbose
```

### Output

The command generates a hierarchical JSON file containing:

```
{
  "metadata": {
    "total_integration_points": <number>,
    "total_crossroads": <number>,
    "analysis_timestamp": <ISO_8601>,
    "files_analyzed": <number>,
    "components_found": <number>
  },
  "codebase_tree": { /* hierarchical component structure */ },
  "global_integration_map": {
    "crossroads": [/* module boundary junctions */],
    "critical_paths": [/* high-integration-count paths */],
    "statistics": { /* aggregated metrics */ }
  }
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - analysis completed successfully |
| 1 | Error - root path not found or analysis failed |

### Performance

Expected analysis times for reference:
- **5-10 files**: <1 second
- **50-100 files**: 2-5 seconds
- **500 files**: 15-30 seconds
- **1000+ files**: 30-60 seconds

Memory usage:
- Typical: 50-200 MB
- Large codebases (1000+ files): <1 GB

### Common Use Cases

#### Generate map for documentation
```bash
python integration_mapper.py --root ./src --output docs/architecture.json
```

#### Analyze specific package
```bash
python integration_mapper.py --root ./src/mypackage --output package_map.json
```

#### Exclude development directories
```bash
python integration_mapper.py \
  --root . \
  --exclude "*/tests/*" \
  --exclude "*/.venv/*" \
  --exclude "*/build/*" \
  --exclude "*/dist/*"
```

### Output File Format

The generated JSON follows the schema defined in `json_schema_design.md`.

Load and query the output:
```python
import json

with open('integration_map.json') as f:
    data = json.load(f)

# Get metadata
print(data['metadata']['total_integration_points'])

# Access component tree
user_module = data['codebase_tree']['myapp']['children']['models']['children']['user']

# Find crossroads
crossroads = data['global_integration_map']['crossroads']

# Analyze critical paths
paths = data['global_integration_map']['critical_paths']
```

---

## Advanced Topics

### Integrating with CI/CD

```yaml
# GitHub Actions example
- name: Generate Integration Map
  run: |
    python integration_mapper.py \
      --root ./src \
      --output architecture_map.json \
      --exclude "*/tests/*"

- name: Upload Artifact
  uses: actions/upload-artifact@v3
  with:
    name: architecture-map
    path: architecture_map.json
```

### Python API

While the tool is designed as a CLI, you can also use it programmatically:

```python
from pathlib import Path
from integration_mapper import IntegrationMapper

mapper = IntegrationMapper(
    root_path=Path('./myproject'),
    exclude_patterns=['*/tests/*', '*/.venv/*']
)

output = mapper.run()

# Access results
print(f"Components: {len(output['codebase_tree'])}")
print(f"Integration points: {output['metadata']['total_integration_points']}")
print(f"Crossroads: {len(output['global_integration_map']['crossroads'])}")
```

---

## Troubleshooting

### "Root path not found"
Ensure the --root directory exists and you have read permissions.

### Slow analysis
- Exclude unnecessary directories (tests, venv, node_modules, build)
- Reduce file count by specifying a more specific root directory
- Check disk I/O performance

### Large memory usage
Reduce codebase size or exclude large packages.

### Incomplete results
Check error messages in output - these may indicate syntax errors in source files.

