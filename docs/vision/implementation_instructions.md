# IMPLEMENTATION INSTRUCTIONS

## Three-Phase Architecture

### Phase 1: Discovery & Hierarchy Building
**Goal:** Build the codebase tree structure with containment relationships

**Steps:**
1. Traverse filesystem from root, collect all `.py` files
2. Parse package structure: detect `__init__.py`, build package hierarchy
3. For each file: `ast.parse()` to get module-level view
4. Build tree structure: `package → module → class → method → nested_function`
5. Assign unique FQN (fully qualified name) to every node
6. Store containment: "module X contains class Y which contains method Z"

**Output:** Hierarchical tree with proper nesting, NOT flat list

### Phase 2: Integration Point Extraction
**Goal:** Map EVERY connection between components with rich context

**For Each File, Extract:**

**Import Integration:**
```python
# For: from myapp.models import User, Product
{
  "source": "current_module",
  "target": "myapp.models",
  "items": ["User", "Product"],
  "usage_count": <count how many times User/Product used>,
  "integration_type": "cross_module_import",
  "line": 5
}
```

**Call Integration (RICH):**
```python
# For: result = user.save(force_insert=True)
{
  "source": "current_function_fqn",
  "target": "User.save",
  "line": 42,
  "args": [
    {"name": "force_insert", "value": "True", "type": "bool"}
  ],
  "return_captured": true,
  "return_var": "result",
  "integration_type": "method_call",
  "data_flow": "result ← user.save() ← database"
}
```

**Attribute Integration:**
```python
# For: user.email = new_email (write)
{
  "source": "current_function",
  "target": "User.email",
  "access_type": "write",
  "line": 65,
  "value_source": "new_email (parameter)",
  "integration_type": "state_mutation"
}

# For: if user.is_active: (read)
{
  "source": "current_function",
  "target": "User.is_active",
  "access_type": "read",
  "line": 67,
  "purpose": "conditional_check",
  "integration_type": "state_access"
}
```

**Inheritance Integration:**
```python
# For: class User(Model, AuthMixin):
{
  "source": "User",
  "targets": ["Model", "AuthMixin"],
  "line": 15,
  "inherited_methods": <list methods from parents>,
  "overridden_methods": <methods User overrides>,
  "integration_type": "inheritance_chain"
}
```

### Phase 3: Flow & Crossroad Analysis
**Goal:** Synthesize integration points into flows and junctions

**Data Flow Construction:**
```python
# Trace complete paths like:
# request → validate() → User() → user.save() → database → serialize() → response

{
  "flow_id": "user_creation_flow",
  "entry_point": "api.create_user",
  "exit_point": "api.create_user (return)",
  "path": [
    {"step": 1, "component": "api.create_user", "action": "receives request"},
    {"step": 2, "component": "utils.validate", "action": "validates data"},
    {"step": 3, "component": "User.__init__", "action": "instantiates model"},
    {"step": 4, "component": "User.save", "action": "persists to database"},
    {"step": 5, "component": "utils.serialize", "action": "formats response"},
    {"step": 6, "component": "api.create_user", "action": "returns response"}
  ],
  "crossroads_encountered": ["api→models", "models→database", "models→utils"],
  "side_effects": ["database_write", "cache_invalidation"]
}
```

**Crossroad Detection:**
```python
# Find where multiple components meet
{
  "crossroad_id": "user_authentication_junction",
  "type": "multi_module_integration",
  "components": ["api.auth", "models.user", "utils.jwt", "middleware.auth"],
  "integration_patterns": [
    "api.auth calls models.User.validate_credentials",
    "api.auth calls utils.jwt.create_token",
    "middleware.auth calls utils.jwt.verify_token",
    "middleware.auth queries models.User"
  ],
  "data_flows_through": 3,
  "criticality": "high"
}
```

## AST Visitor Pattern

### Visitor: HierarchyBuilder
```
visit_Module() → add module node to tree
visit_ClassDef() → add class node under current module
visit_FunctionDef() → add function/method node under current class/module
visit_AsyncFunctionDef() → same as FunctionDef
Track scope stack: [module, class, method] as you traverse
```

### Visitor: IntegrationExtractor
```
visit_Import() → extract import integration with usage tracking
visit_ImportFrom() → extract import with specific items
visit_Call() → RICH call integration:
  - resolve target FQN
  - extract all arguments (positional, keyword, *args, **kwargs)
  - check if return value captured
  - determine data flow direction
  
visit_Attribute() → distinguish Load vs Store context:
  - Load → attribute read
  - Store → attribute write
  - track parent object and attribute chain
  
visit_ClassDef() → extract inheritance:
  - resolve base class FQNs
  - track which methods are defined vs inherited
  
visit_Assign() → track data flow:
  - what variable assigned to
  - where value comes from
  - if it's passed to other functions
```

### Visitor: FlowAnalyzer
```
For each function:
  - Build control flow graph (if/else branches)
  - Track data transformations (input → processing → output)
  - Identify crossroads (calls to other modules)
  - Compute transitive dependencies
```

## Implementation Order

**Iteration 1: Hierarchy + Basic Integration**
- Build codebase tree structure
- Extract imports and basic calls
- Output hierarchical JSON

**Iteration 2: Rich Integration Context**
- Add parameters to call edges
- Add read/write distinction to attributes
- Add usage counts to imports

**Iteration 3: Flow & Crossroad Analysis**
- Build data flow graphs
- Detect crossroads
- Mark critical paths

## Technical Requirements

**Must Haves:**
- Hierarchical nesting (not flat)
- Rich metadata at every integration point
- FQN resolution for all references
- Alias tracking (`import X as Y`)
- Relative import resolution (`.module`, `..parent`)

**Data Structures:**
```python
# Global state during analysis
symbol_table = {}  # FQN → node info
scope_stack = []   # Current traversal context
alias_map = {}     # Alias → original FQN
integration_edges = []  # All connections
call_graph = {}    # Reverse lookup: function → callers
```

## Edge Case Handling

**Dynamic imports:**
```python
# For: importlib.import_module(module_name)
{
  "target": "<dynamic_import>",
  "module_var": "module_name",
  "line": 45,
  "integration_type": "dynamic_import",
  "note": "Cannot resolve statically"
}
```

**Star imports:**
```python
# For: from module import *
{
  "target": "module",
  "items": "*",
  "integration_type": "star_import",
  "note": "Imports all public symbols from module"
}
```

**Decorators:**
```python
# For: @login_required @cache_result def view():
{
  "decorated": "view",
  "decorators": [
    {"name": "login_required", "order": 1, "line": 10},
    {"name": "cache_result", "order": 2, "line": 11}
  ],
  "integration_type": "decorator_chain"
}
```

## Output Format Requirements

**Hierarchical Nesting:**
✅ Package → Module → Class → Method
✅ Each level has `children` dict with nested components
✅ Integration points at appropriate level

**NOT This (Flat):**
```json
{"nodes": [list of 2000 items]}
```

**This (Hierarchical):**
```json
{
  "codebase_tree": {
    "myapp": {
      "children": {
        "models": {
          "children": {
            "user": {
              "children": {
                "User": {
                  "methods": {...}
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

## LLM Optimization

**For Easy Traversal:**
- Consistent key names: `children`, `integration_points`, `data_flows`
- Explicit types: `"type": "class"`, `"type": "method"`
- FQN as `id`: enables instant lookup
- Reverse lookups: `called_by`, `imported_by`, `read_by`, `written_by`

**For Query Patterns:**
LLM should be able to:
- `tree["myapp"]["children"]["models"]["children"]["user"]` → navigate hierarchy
- `node["integration_points"]["called_by"]` → see all callers
- `node["integration_points"]["calls"]` → see all callees
- `global_integration_map["crossroads"]` → see major junctions
