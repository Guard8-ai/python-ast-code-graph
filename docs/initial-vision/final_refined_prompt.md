# FINAL REFINED PROMPT FOR CLAUDE CODE

```
Build a comprehensive Python AST integration mapper that generates a hierarchical JSON map showing EVERY connection between codebase components.

CORE MISSION:
Create a stdlib-only Python script that analyzes a codebase and outputs a rich hierarchical tree showing:
- Complete component hierarchy (packages → modules → classes → methods)
- EVERY integration point with full context (parameters, data flow, purpose)
- All crossroads where components intersect
- Complete data flows from entry to exit points
- Rich metadata enabling instant architecture queries

THE PROBLEM THIS SOLVES:
Claude Code currently must parse files to understand "what calls what", "how do modules integrate", "where does data flow". This wastes cognitive cycles. With this integration map, Claude Code reads the JSON and KNOWS the architecture—no parsing, no inference, no guessing.

INTEGRATION-FIRST PHILOSOPHY:
The value isn't in listing components—it's in mapping HOW they integrate. Every edge must answer: "HOW do these components connect?" Include parameters, data flow direction, integration type, and side effects.

THREE-PHASE ARCHITECTURE:

PHASE 1: HIERARCHY BUILDING
1. Traverse codebase filesystem, collect all .py files
2. Parse package structure (detect __init__.py, build package tree)
3. For each file: ast.parse() and build nested tree structure
4. Assign FQN (fully qualified name) to every component
5. Output structure: codebase_tree with nested children, NOT flat lists

PHASE 2: INTEGRATION EXTRACTION (Rich Context Required)

Import Integration:
{
  "source": "current_module_fqn",
  "target": "imported_module",
  "items": ["SpecificClass", "specific_function"],
  "line": 5,
  "usage_count": 7,  // how many times items are used
  "integration_type": "cross_module_import"
}

Call Integration (MUST BE RICH):
{
  "source": "caller_fqn",
  "target": "callee_fqn",
  "line": 42,
  "args": [
    {"name": "username", "value": "user_data['name']", "type": "str"},
    {"name": "force_insert", "value": "True", "type": "bool"}
  ],
  "return_captured": true,
  "return_var": "result",
  "data_flow": "user_data → User() → user.save() → database",
  "integration_type": "api_to_model_call",
  "side_effects": ["database_write"]
}

Attribute Integration (Read vs Write):
{
  "source": "function_fqn",
  "target": "Class.attribute",
  "access_type": "write",  // or "read"
  "line": 65,
  "value_source": "parameter:new_email",
  "purpose": "state_mutation",
  "integration_type": "attribute_write"
}

Inheritance Integration:
{
  "source": "ChildClass",
  "targets": ["ParentA", "ParentB"],
  "line": 15,
  "inherited_methods": ["save", "delete"],
  "overridden_methods": ["save"],
  "integration_type": "inheritance_chain"
}

PHASE 3: FLOW & CROSSROAD ANALYSIS

Data Flow Construction:
{
  "flow_id": "user_creation_flow",
  "entry_point": "api.create_user",
  "exit_point": "api.create_user.return",
  "path": [
    {"step": 1, "component": "api.create_user", "action": "receives request"},
    {"step": 2, "component": "utils.validate", "action": "validates data"},
    {"step": 3, "component": "User.__init__", "action": "instantiates"},
    {"step": 4, "component": "User.save", "action": "persists"},
    {"step": 5, "component": "utils.serialize", "action": "formats response"}
  ],
  "crossroads": ["api→models", "models→database", "models→utils"],
  "integration_complexity": "high"
}

Crossroad Detection:
{
  "crossroad_id": "api_models_junction",
  "type": "module_boundary",
  "components": ["myapp.api", "myapp.models"],
  "integration_patterns": [
    "API instantiates model classes",
    "API calls model.save() methods",
    "API queries via model managers"
  ],
  "integration_count": 45,
  "criticality": "high"
}

HIERARCHICAL JSON SCHEMA (Required Structure):

{
  "metadata": {
    "total_integration_points": N,
    "total_crossroads": M,
    "analysis_timestamp": ISO_timestamp
  },
  
  "codebase_tree": {
    "package_name": {
      "type": "package",
      "path": "package_name/",
      "exports": ["exported_items"],
      
      "children": {
        "module_name": {
          "type": "module",
          "path": "package_name/module_name.py",
          "imports": [...],
          
          "children": {
            "ClassName": {
              "type": "class",
              "line_range": [10, 50],
              "inherits": ["BaseClass"],
              
              "attributes": {
                "attr_name": {
                  "type": "str",
                  "line": 12,
                  "read_by": ["method1", "method2"],
                  "written_by": ["method3"]
                }
              },
              
              "methods": {
                "method_name": {
                  "type": "method",
                  "line_range": [15, 25],
                  "parameters": [...],
                  "return_type": "ReturnType",
                  
                  "integration_points": {
                    "calls": [...],
                    "called_by": [...],
                    "reads_attributes": [...],
                    "writes_attributes": [...]
                  },
                  
                  "data_flows": [...]
                }
              },
              
              "class_integration_summary": {
                "total_integration_points": X,
                "integration_types": {...}
              }
            }
          }
        }
      }
    }
  },
  
  "global_integration_map": {
    "crossroads": [...],
    "critical_paths": [...],
    "data_flows": [...]
  }
}

EDGE CASE HANDLING (Deterministic):

Dynamic imports: Track as {"target": "<dynamic_import>", "module_var": "variable_name"}
Star imports: Track as {"target": "module", "items": "*"}
Decorators: Track full chain with order
Aliasing: Resolve "import X as Y" throughout
Relative imports: Convert to absolute FQNs using file path
Attribute chains: Break obj.a.b.c() into discrete edges
Nested scopes: Track closures, comprehensions, lambdas

IMPLEMENTATION WORKFLOW:

1. Think hard about the schema structure:
   - How will Claude Code query this?
   - What questions must be instantly answerable?
   
2. Build HierarchyBuilder visitor:
   - visit_Module, visit_ClassDef, visit_FunctionDef
   - Track scope stack, assign FQNs
   - Build nested tree structure

3. Build IntegrationExtractor visitor:
   - visit_Import (with usage tracking)
   - visit_Call (with parameters, data flow)
   - visit_Attribute (distinguish read/write)
   - visit_ClassDef (track inheritance)

4. Build FlowAnalyzer:
   - Trace data flows through function chains
   - Detect module boundary crossroads
   - Mark critical paths

5. Test on small codebase first (5-10 files):
   - Verify hierarchy structure
   - Check integration richness
   - Test Claude Code queries

6. Add CLI:
   --root PATH (required)
   --output FILE (default: integration_map.json)
   --exclude PATTERN (glob to skip)

SUCCESS CRITERIA:

✅ Hierarchical tree structure (nested children, not flat)
✅ EVERY component has FQN and integration_points
✅ Call edges include parameters and data flow
✅ Import edges include usage counts
✅ Attribute edges distinguish read/write
✅ Crossroads section identifies major junctions
✅ Data flows mapped for key paths
✅ Claude Code can answer "what calls X?" by reading JSON (no file parsing)
✅ Developer can understand codebase in 10 minutes using the map

CRITICAL REQUIREMENTS:

1. RICH EDGES: Never output {"source": "A", "target": "B"} without context
2. HIERARCHICAL: Never output flat node lists
3. COMPLETE: Never skip integration points
4. DETERMINISTIC: Pre-resolve aliases, FQNs, flows
5. LLM-OPTIMIZED: Structure for instant queries

WHAT THIS ELIMINATES FOR CLAUDE CODE:
- No file parsing to understand structure
- No inference about connections
- No ambiguity in component relationships
- No cognitive load from "where is X defined?"
- Instant answers to architecture questions

OUTPUT:
Single JSON file (~500-5000 lines depending on codebase size)
Hierarchical tree with rich integration metadata at every node
Ready for Claude Code consumption

NEXT STEP:
Design the complete JSON schema structure first. Think: what architecture questions will Claude Code ask? Structure the JSON to answer those questions instantly.
```
