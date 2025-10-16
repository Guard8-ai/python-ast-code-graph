# Developer Handoff: Codebase Integration Point Mapper

## Executive Summary

You're building a Python AST analyzer that generates a **comprehensive hierarchical integration map** for codebases. The output is a single JSON file that shows EVERY connection, crossroad, and junction between code components—enabling Claude Code (and developers) to understand architecture instantly without parsing files.

**What you're building:** `integration_mapper.py` (~500-700 lines, stdlib-only)  
**Input:** Any Python codebase (path to root directory)  
**Output:** `integration_map.json` (rich hierarchical tree with full integration context)  
**Time estimate:** 8-12 hours of focused development (3 iterations)

---

## The Problem This Solves

### Current Pain Point
Claude Code (and developers) waste cognitive cycles answering:
- "What calls this function?"
- "How do these modules integrate?"
- "Where does data flow from A to B?"
- "What are the major crossroads in this codebase?"

**Without this tool:** Parse files → infer relationships → guess at connections → hope nothing's missed

**With this tool:** Read JSON → know exact integration points → see complete flows → make confident changes

### Why Previous Attempts Failed

❌ **Shallow analysis**: Just listed imports/calls without context  
❌ **Flat structure**: Node lists instead of hierarchical trees  
❌ **Broken edges**: No parameters, no data flow, no purpose  
❌ **Missing crossroads**: Didn't identify where components intersect  
❌ **Poor aliases**: Showed nonsense like "json" unresolved

✅ **This approach**: Rich hierarchical tree with complete integration context at every node

---

## What Success Looks Like

### Primary Success Metrics

**Structural Completeness:**
- [ ] Hierarchical tree (packages → modules → classes → methods)
- [ ] Every component has unique FQN (fully qualified name)
- [ ] Tree reflects actual folder structure

**Integration Richness:**
- [ ] Call edges include: parameters, return values, data flow
- [ ] Import edges include: specific items, usage counts
- [ ] Attribute edges include: read vs write distinction
- [ ] Inheritance edges include: overridden methods

**LLM Usability:**
- [ ] Claude Code can answer "what calls X?" in <2 seconds (just read JSON)
- [ ] Developer can understand codebase in 10 minutes using the map
- [ ] Zero file parsing needed to query architecture

### Validation Test

Give Claude Code the JSON and ask:
1. "Show me everything that calls `User.save`" → Should list all callers with line numbers
2. "What's the data flow for user login?" → Should show complete path
3. "Which modules integrate with the API layer?" → Should list crossroads

If Claude can answer all three instantly by reading JSON: **Success** ✅

---

## Technical Architecture

### Three-Phase Design

```
Phase 1: Hierarchy Building (2-3 hours)
├─ Traverse filesystem
├─ Parse package structure  
├─ Build nested tree (not flat)
└─ Assign FQNs to all components

Phase 2: Integration Extraction (3-4 hours)
├─ Extract imports (with usage tracking)
├─ Extract calls (with parameters + data flow)
├─ Extract attributes (read vs write)
├─ Extract inheritance (with overrides)
└─ Build reverse lookups (called_by, imported_by)

Phase 3: Flow & Crossroad Analysis (2-3 hours)
├─ Trace data flows (entry → exit)
├─ Detect crossroads (module boundaries)
├─ Mark critical paths
└─ Generate global integration map
```

### Core Data Structures

```python
# During analysis (in-memory)
symbol_table: dict[str, NodeInfo]     # FQN → component info
scope_stack: list[str]                # Current traversal context
alias_map: dict[str, str]             # Alias → original FQN
integration_edges: list[dict]         # All connections
call_graph: dict[str, list[str]]      # Reverse lookup: func → callers

# Output (JSON)
{
  "codebase_tree": {...},              # Hierarchical structure
  "global_integration_map": {...}      # Crossroads + flows
}
```

### AST Visitor Pattern

**HierarchyBuilder (Phase 1):**
```python
class HierarchyBuilder(ast.NodeVisitor):
    def visit_Module(self, node):
        # Add module to tree
        # Push module onto scope_stack
        
    def visit_ClassDef(self, node):
        # Add class under current module
        # Track inheritance
        # Push class onto scope_stack
        
    def visit_FunctionDef(self, node):
        # Add function/method under current class/module
        # Assign FQN based on scope_stack
```

**IntegrationExtractor (Phase 2):**
```python
class IntegrationExtractor(ast.NodeVisitor):
    def visit_Import(self, node):
        # Track what's imported
        # Count usage throughout file
        
    def visit_Call(self, node):
        # Resolve target FQN
        # Extract all arguments (positional, keyword, *args, **kwargs)
        # Determine data flow direction
        # Mark side effects
        
    def visit_Attribute(self, node):
        # Distinguish Load (read) vs Store (write)
        # Track attribute chains (obj.a.b.c)
        
    def visit_ClassDef(self, node):
        # Extract base classes
        # Identify overridden methods
```

**FlowAnalyzer (Phase 3):**
```python
class FlowAnalyzer:
    def trace_data_flow(self, function_node):
        # Follow calls from entry to exit
        # Track transformations
        # Identify crossroads
        
    def detect_crossroads(self):
        # Find module boundaries
        # Count integration points
        # Mark critical paths
```

---

## Output Schema Structure

### Hierarchical Tree (Required Format)

```json
{
  "metadata": {
    "total_integration_points": 2847,
    "analysis_timestamp": "2025-10-16T..."
  },
  
  "codebase_tree": {
    "myapp": {
      "type": "package",
      "path": "myapp/",
      
      "children": {
        "models": {
          "type": "module",
          
          "children": {
            "user": {
              "type": "module",
              "path": "myapp/models/user.py",
              "imports": [
                {
                  "source": "django.db.models",
                  "items": ["Model", "CharField"],
                  "usage_count": 15,
                  "line": 1
                }
              ],
              
              "children": {
                "User": {
                  "type": "class",
                  "line_range": [15, 89],
                  "inherits": ["django.db.models.Model"],
                  
                  "methods": {
                    "save": {
                      "type": "method",
                      "line_range": [42, 56],
                      "parameters": [
                        {"name": "self", "type": "User"},
                        {"name": "force_insert", "type": "bool"}
                      ],
                      
                      "integration_points": {
                        "calls": [
                          {
                            "target": "super().save",
                            "line": 45,
                            "args": ["force_insert", "kwargs"],
                            "integration_type": "inheritance_chain"
                          },
                          {
                            "target": "myapp.utils.logger.log",
                            "line": 54,
                            "args": ["self.username", "action='save'"],
                            "integration_type": "cross_module_junction"
                          }
                        ],
                        
                        "called_by": [
                          {
                            "source": "myapp.api.create_user",
                            "line": 78,
                            "integration_type": "api_to_model"
                          }
                        ],
                        
                        "reads_attributes": [
                          {"attr": "self.username", "line": 43}
                        ],
                        
                        "writes_attributes": [
                          {"attr": "self.updated_at", "line": 53}
                        ]
                      },
                      
                      "data_flows": [
                        {
                          "path": ["request_data", "self.validate()", "super().save()", "database"],
                          "crossroads": ["api→models", "models→database"]
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
  },
  
  "global_integration_map": {
    "crossroads": [
      {
        "id": "api_to_models_junction",
        "components": ["myapp.api", "myapp.models"],
        "integration_count": 45,
        "patterns": ["API calls model.save()", "API queries managers"]
      }
    ],
    
    "critical_paths": [
      {
        "path_id": "user_authentication_flow",
        "entry": "api.auth.login",
        "exit": "api.auth.set_cookie",
        "components": ["api", "models", "utils"]
      }
    ]
  }
}
```

---

## Implementation Roadmap

### Iteration 1: Hierarchical Structure (2-3 hours)

**Goal:** Build correct tree structure with basic integration

**Tasks:**
1. Set up CLI with argparse (`--root`, `--output`, `--exclude`)
2. Implement file discovery (pathlib glob for `*.py`)
3. Build HierarchyBuilder visitor
4. Output nested JSON structure
5. Test on small codebase (5-10 files)

**Validation:** Tree reflects folder structure, all components have FQNs

### Iteration 2: Rich Integration (3-4 hours)

**Goal:** Add full context to every edge

**Tasks:**
1. Enhance IntegrationExtractor for calls with parameters
2. Add usage counting for imports
3. Implement read/write distinction for attributes
4. Add reverse lookups (`called_by`, `imported_by`)
5. Test edge richness on real codebase

**Validation:** Call edges show parameters, imports show usage counts

### Iteration 3: Flow & Crossroads (2-3 hours)

**Goal:** Analyze integration patterns

**Tasks:**
1. Implement FlowAnalyzer to trace data paths
2. Detect module boundary crossroads
3. Mark critical paths
4. Add global_integration_map section
5. Test on medium codebase (100+ files)

**Validation:** Flows are complete, crossroads identified

---

## Edge Cases & Solutions

### Dynamic Imports
```python
# For: importlib.import_module(module_name)
{
  "target": "<dynamic_import>",
  "module_var": "module_name",
  "note": "Cannot resolve statically"
}
```

### Star Imports
```python
# For: from module import *
{
  "target": "module",
  "items": "*",
  "note": "Imports all public symbols"
}
```

### Aliasing
```python
# For: import pandas as pd
# Resolve all uses of 'pd' to 'pandas'
alias_map["pd"] = "pandas"
# When encountering pd.DataFrame, resolve to pandas.DataFrame
```

### Relative Imports
```python
# For: from ..parent import something
# Calculate absolute path:
# Current file: /project/myapp/submodule/file.py
# .. goes up to /project/myapp
# Absolute: myapp.parent.something
```

### Attribute Chains
```python
# For: obj.a.b.c()
# Break into discrete edges:
edges = [
  {"source": "current_func", "target": "obj.a", "type": "attribute"},
  {"source": "current_func", "target": "obj.a.b", "type": "attribute"},
  {"source": "current_func", "target": "obj.a.b.c", "type": "call"}
]
```

### Decorators
```python
# For: @login_required @cache_result def view():
{
  "decorated": "view",
  "decorators": [
    {"name": "login_required", "order": 1},
    {"name": "cache_result", "order": 2}
  ]
}
```

---

## Key Technical Decisions

### Why Hierarchical Tree?
**Decision:** Nested `children` dicts, not flat node lists  
**Rationale:** Mirrors how developers think about code structure; enables intuitive navigation; reflects actual folder hierarchy  
**Trade-off:** Slightly more complex to build, but massively better for LLM consumption

### Why Rich Edges?
**Decision:** Include parameters, data flow, side effects on every edge  
**Rationale:** "Function A calls B" is useless; "A passes user_id to B which queries DB" is actionable  
**Trade-off:** Larger JSON files, but eliminates need for file parsing

### Why Three Passes?
**Decision:** Discovery → Integration → Flow analysis  
**Rationale:** Forward references require symbol table before resolving; flow analysis needs complete call graph  
**Trade-off:** Slower analysis, but complete and correct output

### Why Stdlib-Only?
**Decision:** No external dependencies (networkx, graphviz, etc.)  
**Rationale:** Easy deployment; no version conflicts; pure Python portability  
**Trade-off:** More code to write, but total control and zero dependencies

---

## Validation Checklist

Before considering the tool "done", verify:

### Structural Checks
- [ ] Load JSON without errors
- [ ] Navigate tree: `tree["pkg"]["children"]["mod"]["children"]["Class"]`
- [ ] Every component has unique FQN
- [ ] Tree depth matches folder structure

### Integration Checks
- [ ] 10 random function calls → all have parameters listed
- [ ] 10 random imports → all have usage counts
- [ ] 10 random attributes → read/write distinguished
- [ ] 5 classes with inheritance → overrides tracked

### LLM Usability Checks
- [ ] Claude Code answers "what calls X?" in <2 seconds
- [ ] Claude Code answers "show hierarchy of Y?" instantly
- [ ] Claude Code traces data flow without parsing files

### Performance Checks
- [ ] 100 files analyzed in <15 seconds
- [ ] 500 files analyzed in <30 seconds
- [ ] JSON output <10MB for 1000 files
- [ ] Memory usage <1GB during analysis

---

## Common Pitfalls & How to Avoid

### Pitfall 1: Flat Output
**Symptom:** `{"nodes": [2000 items]}`  
**Fix:** Use nested `children` dicts at every level

### Pitfall 2: Shallow Edges
**Symptom:** `{"source": "A", "target": "B", "type": "call"}`  
**Fix:** Add parameters, data_flow, integration_type, line numbers

### Pitfall 3: Broken Aliases
**Symptom:** Seeing "json" or "pd" unresolved in output  
**Fix:** Maintain alias_map per module, resolve before adding edges

### Pitfall 4: Missing Reverse Lookups
**Symptom:** Can find what X calls, but not what calls X  
**Fix:** Build `called_by`, `imported_by`, `read_by`, `written_by` lists

### Pitfall 5: Incomplete Flows
**Symptom:** Flow paths have gaps  
**Fix:** Trace through entire call chain, mark where resolution fails

---

## Testing Strategy

### Phase 1 Test: Small Codebase
- Use 3-5 file test project with known structure
- Manually verify every component in tree
- Check all integration points against source code

### Phase 2 Test: Medium Codebase
- Use 50-100 file real project
- Spot-check 20 random integration points
- Verify crossroads match architectural boundaries

### Phase 3 Test: Large Codebase
- Use 500+ file production codebase
- Performance test: measure analysis time
- LLM test: Can Claude Code answer architecture questions?

---

## Dependencies & Environment

**Requirements:**
- Python 3.8+ (for ast module features)
- Stdlib only: `ast`, `pathlib`, `json`, `argparse`, `sys`
- No external packages

**Development:**
```bash
# Clone/create project
mkdir integration_mapper && cd integration_mapper

# Create main script
touch integration_mapper.py

# Test on sample project
python integration_mapper.py --root /path/to/test/project --output map.json

# Validate output
python -m json.tool map.json > /dev/null  # Check valid JSON
```

---

## CLI Contract

```bash
python integration_mapper.py --root PATH [OPTIONS]

Required:
  --root PATH           Path to codebase root directory

Optional:
  --output FILE         Output JSON file (default: integration_map.json)
  --exclude PATTERN     Glob pattern to exclude files (e.g., "*/tests/*")
  --verbose            Show progress during analysis

Example:
python integration_mapper.py --root ./myproject --output arch.json --exclude "*/migrations/*"
```

---

## Integration with Claude Code

### Usage Pattern

1. **Generate map:**
   ```bash
   python integration_mapper.py --root /path/to/project --output codebase_map.json
   ```

2. **Load into Claude Code:**
   ```
   I've generated an integration map of my codebase. Here's the JSON:
   [paste codebase_map.json]
   
   Using this map, show me all functions that call User.save
   ```

3. **Claude Code responds:**
   ```
   Based on the integration map, User.save is called by:
   - myapp.api.user_endpoints.create_user (line 78)
   - myapp.views.profile.update_profile (line 45)
   - myapp.tasks.sync_users (line 112)
   ```

**Result:** Instant architectural queries with zero file parsing

---

## Success Criteria Summary

✅ **You're done when:**
1. JSON loads without errors
2. Tree is hierarchical (nested children)
3. All components have integration_points
4. Edges have rich context (parameters, data flow)
5. Crossroads section exists and is populated
6. Claude Code can answer "what calls X?" instantly
7. Developer can understand codebase in 10 minutes

---

## Next Steps

1. **Read artifacts** (Vision, Schema, Implementation Instructions)
2. **Set up project** (create integration_mapper.py)
3. **Iteration 1** (build hierarchical tree)
4. **Iteration 2** (add rich integration)
5. **Iteration 3** (flow & crossroad analysis)
6. **Validate** (use follow-up prompts to refine)

---

## Questions to Ask If Stuck

- Is my output hierarchical or flat? (Should be nested)
- Do my edges have context? (Should show parameters, data flow)
- Can I answer "what calls X?" (Should have reverse lookups)
- Are aliases resolved? (Should not see "json" or "pd" raw)
- Do flows trace end-to-end? (Should show complete paths)

---

## Final Notes

**This is not a perfect analyzer—it's a useful one.** Ship something that works in Iteration 1, then refine based on real usage. The goal is enabling Claude Code to understand architecture instantly, not building the ultimate static analysis tool.

**Developer sovereignty:** You decide what to do with the integration map. No best practices enforced. No architecture judgments. Pure data about how your codebase connects.

**Quick and functional:** Get a working map in 8-12 hours. Refine over time based on what you actually need.

---

## References

- **Vision Artifact**: Problem statement and philosophy
- **Schema Artifact**: Complete JSON structure examples
- **Implementation Instructions**: Three-phase architecture details
- **Success Criteria**: Validation tests and metrics
- **Follow-Up Prompts**: 8 iterative refinement prompts
- **Final Refined Prompt**: Ready-to-use Claude Code prompt

Good luck! You're building something that will transform how you (and Claude Code) understand codebases. 🚀