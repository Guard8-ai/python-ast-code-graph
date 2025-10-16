# Integration Mapper: Developer Quick-Start Guide

**Everything a developer needs to know to use, understand, and verify Integration Mapper in 10 minutes.**

---

## 🎯 Three Core Questions This Guide Answers

1. **How do I use it?** → See Section: [Running Integration Mapper](#section-1-how-to-use-it)
2. **What output should I expect?** → See Section: [Understanding the Output](#section-2-what-the-output-looks-like)
3. **How do I know it worked?** → See Section: [Verification Checklist](#section-3-verification-checklist)

---

## SECTION 1: HOW TO USE IT

### Quick Command Reference

```bash
# Basic usage
python integration_mapper.py --root ./myproject

# Specify output file
python integration_mapper.py --root ./myproject --output architecture.json

# Exclude test and build files
python integration_mapper.py \
  --root ./myproject \
  --output map.json \
  --exclude "*/tests/*" \
  --exclude "*/venv/*" \
  --exclude "*/__pycache__/*"

# Verbose output (see progress)
python integration_mapper.py --root ./myproject --verbose
```

### Real-World Scenarios

#### Scenario 1: Analyze a Django Project
```bash
python integration_mapper.py \
  --root ./django_app \
  --output django_map.json \
  --exclude "*/migrations/*" \
  --exclude "*/venv/*" \
  --exclude "*/static/*" \
  --exclude "*/media/*"
```

**What happens:**
- Discovers all `.py` files in `django_app/`
- Excludes migrations, virtual env, static files
- Analyzes views, models, serializers, utils
- Generates `django_map.json` with complete architecture

#### Scenario 2: Analyze a Specific Package
```bash
python integration_mapper.py \
  --root ./src/mypackage \
  --output package_analysis.json
```

**What happens:**
- Only analyzes files under `src/mypackage/`
- Creates focused integration map
- Shows internal package structure and dependencies

#### Scenario 3: Analyze Everything (Including Tests)
```bash
python integration_mapper.py --root . --output full_map.json
```

**What happens:**
- Analyzes entire codebase
- Includes test files
- Larger output, more integration points
- Good for comprehensive architecture review

### CLI Arguments Explained

| Argument | Required | Example | What It Does |
|----------|----------|---------|------------|
| `--root` | ✅ YES | `--root ./src` | Root directory to analyze |
| `--output` | ❌ NO | `--output map.json` | Where to save JSON (default: `integration_map.json`) |
| `--exclude` | ❌ NO | `--exclude "*/tests/*"` | Skip files matching pattern (repeatable) |
| `--verbose` | ❌ NO | `--verbose` | Show progress during analysis |
| `--help` | ❌ NO | `--help` | Show help message |

### Exit Codes

```bash
$ python integration_mapper.py --root ./project
# Exit code 0 = Success ✅
# Exit code 1 = Error (root not found, analysis failed) ❌
```

Check exit code:
```bash
python integration_mapper.py --root ./project
echo "Exit code: $?"  # 0 or 1
```

---

## SECTION 2: WHAT THE OUTPUT LOOKS LIKE

### Output File Structure (High Level)

The tool generates a JSON file with three main sections:

```json
{
  "metadata": { /* Overview statistics */ },
  "codebase_tree": { /* Hierarchical component structure */ },
  "global_integration_map": { /* Architecture-level insights */ }
}
```

### 2A: METADATA Section

**What it contains:** High-level statistics about the analysis

```json
{
  "metadata": {
    "total_integration_points": 247,
    "total_crossroads": 8,
    "analysis_timestamp": "2025-10-16T14:30:00Z",
    "files_analyzed": 45,
    "components_found": 156
  }
}
```

**What each field means:**
- `total_integration_points`: Number of edges (imports, calls, attributes, inheritance)
- `total_crossroads`: Major module boundary junctions discovered
- `analysis_timestamp`: When the analysis ran
- `files_analyzed`: How many .py files were processed
- `components_found`: Total functions, classes, modules discovered

**Example interpretation:**
- ✅ 45 files analyzed → Good coverage
- ✅ 156 components found → Substantial codebase
- ✅ 247 integration points → Well-integrated system
- ✅ 8 crossroads → Multiple architectural layers

### 2B: CODEBASE_TREE Section

**What it contains:** Hierarchical structure of your code (packages → modules → classes → methods)

```json
{
  "codebase_tree": {
    "myapp": {
      "type": "package",
      "path": "myapp/",
      "children": {
        "models": {
          "type": "module",
          "path": "myapp/models.py",
          "imports": [
            {
              "source": "django.db.models",
              "items": ["Model", "CharField"],
              "usage_count": 12,
              "line": 1,
              "integration_type": "framework_import"
            }
          ],
          "children": {
            "User": {
              "type": "class",
              "line_range": [5, 50],
              "methods": {
                "save": {
                  "type": "method",
                  "line_range": [20, 30],
                  "parameters": [
                    {"name": "self", "type": "User"}
                  ],
                  "integration_points": {
                    "calls": [
                      {
                        "target": "super().save",
                        "line": 25,
                        "args": [],
                        "integration_type": "inheritance_chain"
                      }
                    ],
                    "called_by": [
                      {
                        "source": "myapp.api.create_user",
                        "line": 42
                      }
                    ]
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**How to read this:**

1. **Navigate the hierarchy:** `myapp` (package) → `models` (module) → `User` (class) → `save` (method)
2. **See imports:** What each module imports (line number, usage count)
3. **Understand calls:** Who calls whom (e.g., `api.create_user` calls `User.save` at line 42)
4. **Track inheritance:** What classes inherit from (e.g., `User` uses `super().save`)

**Key insight:** Everything is connected with line numbers, so you can jump straight to code in your editor!

### 2C: GLOBAL_INTEGRATION_MAP Section

**What it contains:** High-level architecture view (crossroads, critical paths, data flows)

```json
{
  "global_integration_map": {
    "crossroads": [
      {
        "id": "api_models_junction",
        "components": ["myapp.api", "myapp.models"],
        "integration_count": 45,
        "criticality": "high",
        "description": "API layer creates and queries model instances"
      },
      {
        "id": "models_database",
        "components": ["myapp.models", "database"],
        "integration_count": 87,
        "criticality": "critical"
      }
    ],

    "critical_paths": [
      {
        "id": "path_user_creation",
        "entry_point": "myapp.api.create_user",
        "call_count": 12,
        "complexity": "high"
      },
      {
        "id": "path_user_auth",
        "entry_point": "myapp.auth.login",
        "call_count": 8,
        "complexity": "medium"
      }
    ],

    "statistics": {
      "total_components": 156,
      "total_integration_points": 247
    }
  }
}
```

**What each section means:**

**Crossroads:**
- Where multiple modules/layers interact
- **High criticality** = careful refactoring needed
- **Integration count** = how many edges cross this boundary

**Critical Paths:**
- Functions/methods that are called frequently
- **Entry points** for understanding data flow
- **Complexity** rating based on call count

---

## SECTION 3: VERIFICATION CHECKLIST

### How to Know It Worked Properly

After running the analyzer, use this checklist to verify success:

```
✅ File checks:
   □ Output file exists and has content
   □ File size > 100 bytes (not empty)
   □ File is valid JSON (can parse it)

✅ Metadata checks:
   □ total_integration_points > 0
   □ files_analyzed > 0
   □ components_found > 0
   □ analysis_timestamp is recent

✅ Tree structure checks:
   □ codebase_tree is not empty
   □ Has top-level packages or modules
   □ Each node has "type" and "children" fields
   □ Can navigate: package → module → class → method

✅ Integration edges checks:
   □ Crossroads count > 0 (unless single-file project)
   □ Critical_paths count > 0
   □ Some imports captured
   □ Some function calls captured

✅ No errors:
   □ No error messages in console
   □ Exit code = 0 (success)
   □ Analysis completed successfully message
```

### Quick Verification Script

Run this after analyzing:

```bash
# 1. Check file exists and has content
ls -lh integration_map.json

# 2. Validate JSON is parseable
python -m json.tool integration_map.json > /dev/null && echo "✅ Valid JSON"

# 3. Check key metrics
python << 'EOF'
import json
with open('integration_map.json') as f:
    data = json.load(f)

meta = data['metadata']
print(f"✅ Files analyzed: {meta['files_analyzed']}")
print(f"✅ Components found: {meta['components_found']}")
print(f"✅ Integration points: {meta['total_integration_points']}")
print(f"✅ Crossroads: {meta['total_crossroads']}")

# Verify structure
tree = data['codebase_tree']
print(f"✅ Tree has {len(tree)} top-level packages/modules")

# Verify global map
gmap = data['global_integration_map']
print(f"✅ Crossroads: {len(gmap['crossroads'])}")
print(f"✅ Critical paths: {len(gmap['critical_paths'])}")
EOF
```

### Success Indicators

#### ✅ Good Analysis (Project with 50-100 files)

```
Files analyzed: 45
Components found: 156
Integration points: 247
Crossroads: 8
Crossroads:
  • api ↔ models: 45 edges (HIGH criticality)
  • models ↔ database: 87 edges (CRITICAL criticality)
  • models ↔ utils: 23 edges (MEDIUM criticality)
Critical paths:
  • api.create_user: 12 calls
  • models.User.save: 8 calls
  • auth.login: 6 calls
```

**Interpretation:** ✅ **HEALTHY SYSTEM**
- Good file/component ratio
- Multiple integration layers detected
- Clear entry points identified

#### ⚠️ Small/Minimal Analysis (Project with 5-10 files)

```
Files analyzed: 7
Components found: 18
Integration points: 25
Crossroads: 2
Crossroads:
  • api ↔ models: 10 edges
Critical paths:
  • api.endpoints: 6 calls
```

**Interpretation:** ✅ **NORMAL FOR SMALL PROJECT**
- Fewer components is expected
- Fewer crossroads is expected
- Still shows integration structure

#### ❌ Red Flags (Something Wrong)

```
Files analyzed: 45
Components found: 0          ← ❌ NO COMPONENTS FOUND
Integration points: 0        ← ❌ NO EDGES FOUND
Crossroads: 0

OR

Error processing /path/to/file.py: ...
```

**What to do:**
1. Check if files are valid Python (no syntax errors)
2. Verify --root path is correct
3. Check file permissions
4. Try smaller subset of code first

---

## SECTION 4: COMMON DEVELOPER WORKFLOWS

### Workflow A: Quick Architecture Review

```bash
# Step 1: Generate map
python integration_mapper.py --root ./src --output arch.json

# Step 2: Check metadata
python -c "import json; d=json.load(open('arch.json')); print(d['metadata'])"

# Step 3: Review crossroads (major boundaries)
python -c "import json; d=json.load(open('arch.json'));
import pprint; pprint.pprint(d['global_integration_map']['crossroads'])"

# Step 4: Review critical paths (entry points)
python -c "import json; d=json.load(open('arch.json'));
import pprint; pprint.pprint(d['global_integration_map']['critical_paths'])"
```

### Workflow B: Before Refactoring

```bash
# Generate map of current code
python integration_mapper.py --root ./src --output before_refactor.json

# Show what calls the module you're about to refactor
python << 'EOF'
import json
data = json.load(open('before_refactor.json'))

# Find all references to target_function
target = "myapp.utils.database_query"
tree = data['codebase_tree']

# (would navigate tree to find all callers)
print(f"Analyzing calls to {target}")
EOF
```

### Workflow C: New Developer Onboarding

```bash
# Generate complete architecture map
python integration_mapper.py --root . --output full_architecture.json

# Share architecture overview
echo "Architecture Summary:"
echo "===================="
python << 'EOF'
import json
data = json.load(open('full_architecture.json'))
m = data['metadata']
print(f"Codebase size: {m['files_analyzed']} files, {m['components_found']} components")
print(f"Integration complexity: {m['total_integration_points']} edges")
print(f"Architectural layers: {m['total_crossroads']} boundaries")
print("\nMajor entry points:")
for path in data['global_integration_map']['critical_paths'][:5]:
    print(f"  • {path['entry_point']}")
EOF
```

---

## SECTION 5: INTERPRETING KEY METRICS

### Files Analyzed vs Components Found

```
Expected ratios:
- Small project (5-10 files): 10-30 components per file
- Medium project (50-100 files): 3-5 components per file
- Large project (500+ files): 1-3 components per file

Example:
- 45 files, 156 components = 3.5 components/file ✅ NORMAL
- 45 files, 450 components = 10 components/file ⚠️ CHECK FOR CODE GENERATION
- 45 files, 20 components = 0.4 components/file ⚠️ MANY EMPTY/COMMENT FILES
```

### Integration Points Interpretation

```
Expected ranges:
- 5-10 file project: 20-50 edges
- 50-100 file project: 100-400 edges
- 500+ file project: 1000-5000 edges

Example:
- 45 files, 247 edges = 5.5 edges/file ✅ NORMAL (well-integrated)
- 45 files, 1000 edges = 22 edges/file ⚠️ VERY HIGH COUPLING
- 45 files, 15 edges = 0.3 edges/file ⚠️ VERY LOW COUPLING (check if correct)
```

### Crossroads Interpretation

```
Crossroads > files analyzed × 0.1 = Healthy multi-layer architecture ✅
Crossroads < files analyzed × 0.01 = Single-layer or monolithic ⚠️
Crossroads > files analyzed × 0.5 = Overly modularized ⚠️
```

---

## SECTION 6: TROUBLESHOOTING

### Problem: "Root path not found"
```bash
# Solution: Verify path exists
ls -la ./myproject
python integration_mapper.py --root ./myproject
```

### Problem: No output file created
```bash
# Check if analysis failed
python integration_mapper.py --root . --verbose
# Look for error messages

# Verify Python syntax in your code
python -m py_compile ./myproject/*.py
```

### Problem: Very large JSON output (>10MB)
```bash
# Solution: Exclude unnecessary directories
python integration_mapper.py \
  --root . \
  --exclude "*/tests/*" \
  --exclude "*/.venv/*" \
  --exclude "*/migrations/*"
```

### Problem: Analysis takes >60 seconds
```bash
# Solution: Analyze smaller subset
python integration_mapper.py --root ./src/specific_package

# Or exclude large directories
python integration_mapper.py \
  --root . \
  --exclude "*/tests/*" \
  --exclude "*/__pycache__/*" \
  --verbose
```

---

## SECTION 7: QUICK REFERENCE CARD

```
╔════════════════════════════════════════════════════════════════╗
║         INTEGRATION MAPPER: QUICK REFERENCE                   ║
╚════════════════════════════════════════════════════════════════╝

BASIC USAGE:
  python integration_mapper.py --root ./myproject

WITH OPTIONS:
  python integration_mapper.py \
    --root ./myproject \
    --output map.json \
    --exclude "*/tests/*" \
    --verbose

VERIFY IT WORKED:
  ✅ Output file exists: ls -lh integration_map.json
  ✅ Valid JSON: python -m json.tool integration_map.json
  ✅ Has content: grep "total_integration_points" integration_map.json
  ✅ Exit code 0: echo $?

WHAT TO EXPECT:
  • metadata: file count, component count, edge count
  • codebase_tree: hierarchical structure (pkg→mod→class→method)
  • global_integration_map: crossroads, critical paths, statistics

SUCCESS INDICATORS:
  ✅ Files analyzed > 0
  ✅ Components found > 0
  ✅ Integration points > 0
  ✅ Can parse JSON output
  ✅ No error messages

RED FLAGS:
  ❌ Components found = 0
  ❌ Error messages in output
  ❌ JSON won't parse
  ❌ File size = 0 bytes
  ❌ Exit code = 1
```

---

## APPENDIX: Example Analysis Session

```bash
# 1. Navigate to project
cd /home/developer/myproject

# 2. Run analyzer
$ python integration_mapper.py --root ./src --output architecture.json --verbose
🚀 Starting Integration Mapper Analysis
Root: /home/developer/myproject/src

Discovered 45 Python files
Phase 1: Building hierarchy...
Built hierarchy with 156 components
Phase 2: Extracting integration points...
Extracted 247 integration edges
Phase 3: Analyzing flows and crossroads...
Identified 8 crossroads and 12 critical paths

✅ Analysis complete!
Output: /home/developer/myproject/architecture.json
Integration points: 247
Crossroads: 8

# 3. Quick verification
$ python -m json.tool architecture.json > /dev/null && echo "✅ Valid JSON"
✅ Valid JSON

# 4. Check metrics
$ python << 'EOF'
import json
with open('architecture.json') as f:
    d = json.load(f)
m = d['metadata']
print(f"📊 Analysis Results:")
print(f"   Files: {m['files_analyzed']}")
print(f"   Components: {m['components_found']}")
print(f"   Edges: {m['total_integration_points']}")
print(f"   Crossroads: {m['total_crossroads']}")
print(f"\n✅ Analysis successful!")
EOF
📊 Analysis Results:
   Files: 45
   Components: 156
   Edges: 247
   Crossroads: 8

✅ Analysis successful!

# 5. Ready for use!
# Now integrate with Claude Code or tools
```

---

**Happy analyzing! 🚀**

For detailed information, see:
- `CLAUDE.md` - Project guidance
- `CLI_USAGE.md` - Complete CLI documentation
- `json_schema_design.md` - Output schema details
- `IMPLEMENTATION.md` - Architecture deep-dive
