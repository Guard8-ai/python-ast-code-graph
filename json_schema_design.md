# Integration Mapper: JSON Schema Design

## Schema Overview

The output JSON is a hierarchical tree structure enabling instant architecture queries without file parsing.

```
{
  "metadata": { ... },
  "codebase_tree": { ... },
  "global_integration_map": { ... }
}
```

---

## 1. METADATA Section

Provides high-level analysis summary.

```json
{
  "metadata": {
    "total_integration_points": 2847,
    "total_crossroads": 12,
    "analysis_timestamp": "2025-10-16T14:30:00Z",
    "python_version": "3.8+",
    "files_analyzed": 156,
    "packages": 8,
    "modules": 47,
    "classes": 234,
    "functions": 891
  }
}
```

**Purpose:** Quick overview of codebase complexity

---

## 2. CODEBASE_TREE Section

Hierarchical nested structure: Package → Module → Class → Method

### Tree Node Structure (Generic)

Every node has:
```json
{
  "type": "package|module|class|method|function",
  "path": "path/to/file.py or package/",
  "line_range": [start, end],
  "docstring": "Optional docstring summary",
  "children": { /* nested components */ },
  "integration_points": { /* edges to other components */ }
}
```

### Example: Full Hierarchy (myapp/models/user.py)

```json
{
  "codebase_tree": {
    "myapp": {
      "type": "package",
      "path": "myapp/",
      "exports": ["models", "api", "utils"],
      "children": {
        "models": {
          "type": "package",
          "path": "myapp/models/",
          "children": {
            "user": {
              "type": "module",
              "path": "myapp/models/user.py",
              "imports": [
                {
                  "source": "django.db.models",
                  "items": ["Model", "CharField", "EmailField"],
                  "usage_count": 12,
                  "line": 1,
                  "integration_type": "framework_import"
                },
                {
                  "source": "myapp.utils.validators",
                  "items": ["validate_email"],
                  "usage_count": 2,
                  "line": 3,
                  "integration_type": "cross_module_import"
                }
              ],
              "children": {
                "User": {
                  "type": "class",
                  "line_range": [15, 120],
                  "inherits": ["django.db.models.Model"],
                  "docstring": "User model representing application users",

                  "attributes": {
                    "username": {
                      "type": "CharField",
                      "line": 18,
                      "read_by": ["get_profile", "authenticate"],
                      "written_by": ["__init__", "update_profile"]
                    },
                    "email": {
                      "type": "EmailField",
                      "line": 20,
                      "read_by": ["send_email", "validate"],
                      "written_by": ["__init__", "change_email"]
                    }
                  },

                  "methods": {
                    "save": {
                      "type": "method",
                      "line_range": [42, 56],
                      "parameters": [
                        {"name": "self", "type": "User"},
                        {"name": "force_insert", "type": "bool", "default": "False"}
                      ],
                      "return_type": "None",

                      "integration_points": {
                        "calls": [
                          {
                            "target": "validate_email",
                            "target_fqn": "myapp.utils.validators.validate_email",
                            "line": 44,
                            "args": [
                              {"name": "email", "value": "self.email", "type": "str"}
                            ],
                            "return_captured": false,
                            "data_flow": "self.email → validate_email() [validation]",
                            "integration_type": "utility_call",
                            "side_effects": []
                          },
                          {
                            "target": "super().save",
                            "target_fqn": "django.db.models.Model.save",
                            "line": 48,
                            "args": [
                              {"name": "force_insert", "value": "force_insert", "type": "bool"}
                            ],
                            "return_captured": false,
                            "data_flow": "User instance → persist to database",
                            "integration_type": "inheritance_chain",
                            "side_effects": ["database_write", "cache_invalidation"]
                          }
                        ],

                        "called_by": [
                          {
                            "source": "myapp.api.user_endpoints.create_user",
                            "source_fqn": "myapp.api.user_endpoints.create_user",
                            "line": 78,
                            "context": "API endpoint creates and saves new user",
                            "integration_type": "api_to_model"
                          },
                          {
                            "source": "myapp.views.profile.update_profile",
                            "source_fqn": "myapp.views.profile.update_profile",
                            "line": 45,
                            "context": "View updates existing user",
                            "integration_type": "view_to_model"
                          }
                        ],

                        "reads_attributes": [
                          {"attr": "self.username", "line": 43, "purpose": "validation"},
                          {"attr": "self.email", "line": 44, "purpose": "validation"}
                        ],

                        "writes_attributes": [
                          {"attr": "self.updated_at", "line": 50, "source": "datetime.now()"}
                        ]
                      },

                      "data_flows": [
                        {
                          "flow_id": "user_save_flow",
                          "entry_point": "User.save",
                          "exit_point": "User.save (return)",
                          "steps": [
                            {
                              "step": 1,
                              "component": "User.save",
                              "action": "receives user instance"
                            },
                            {
                              "step": 2,
                              "component": "validate_email",
                              "action": "validates email address"
                            },
                            {
                              "step": 3,
                              "component": "super().save",
                              "action": "persists to database"
                            },
                            {
                              "step": 4,
                              "component": "User.save",
                              "action": "returns (implicit None)"
                            }
                          ],
                          "crossroads": ["models → utils", "models → database"],
                          "integration_complexity": "medium"
                        }
                      ]
                    },

                    "get_profile": {
                      "type": "method",
                      "line_range": [60, 75],
                      "parameters": [{"name": "self", "type": "User"}],
                      "return_type": "Dict[str, Any]",
                      "integration_points": {
                        "calls": [
                          {
                            "target": "myapp.models.profile.Profile.objects.get",
                            "line": 62,
                            "args": [{"name": "user_id", "value": "self.id"}],
                            "return_captured": true,
                            "return_var": "profile",
                            "data_flow": "user.id → Profile query → profile object",
                            "integration_type": "orm_query",
                            "side_effects": ["database_read"]
                          }
                        ],
                        "called_by": [
                          {
                            "source": "myapp.api.user_endpoints.get_user",
                            "line": 89
                          }
                        ]
                      }
                    }
                  },

                  "class_integration_summary": {
                    "total_integration_points": 47,
                    "integration_types": {
                      "calls": 12,
                      "called_by": 8,
                      "attribute_reads": 15,
                      "attribute_writes": 5,
                      "inheritance": 1
                    },
                    "critical": true
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

---

## 3. GLOBAL_INTEGRATION_MAP Section

High-level architectural view: crossroads, critical paths, major flows.

```json
{
  "global_integration_map": {
    "crossroads": [
      {
        "crossroad_id": "api_to_models_junction",
        "type": "module_boundary",
        "components": ["myapp.api", "myapp.models"],
        "integration_patterns": [
          "API instantiates model classes",
          "API calls model.save() methods",
          "API queries via model managers",
          "API serializes model instances"
        ],
        "integration_count": 45,
        "criticality": "critical",
        "description": "API layer creates, reads, updates user models"
      },
      {
        "crossroad_id": "models_to_database",
        "type": "layer_transition",
        "components": ["myapp.models", "database"],
        "integration_patterns": [
          "ORM saves to database",
          "ORM queries from database",
          "Transaction handling"
        ],
        "integration_count": 87,
        "criticality": "critical",
        "description": "Model persistence layer"
      },
      {
        "crossroad_id": "models_to_utils",
        "type": "utility_junction",
        "components": ["myapp.models", "myapp.utils"],
        "integration_patterns": [
          "Models call validation utilities",
          "Models use serialization utilities",
          "Models use logging utilities"
        ],
        "integration_count": 23,
        "criticality": "medium"
      }
    ],

    "critical_paths": [
      {
        "path_id": "user_creation_flow",
        "description": "Complete user creation from API to database",
        "entry_point": "myapp.api.user_endpoints.create_user",
        "exit_point": "database (User record saved)",
        "steps": [
          {
            "step": 1,
            "component": "api.user_endpoints.create_user",
            "action": "receives HTTP request"
          },
          {
            "step": 2,
            "component": "api.serializers.UserSerializer",
            "action": "deserializes JSON to data dict"
          },
          {
            "step": 3,
            "component": "utils.validators.validate_user_data",
            "action": "validates all fields"
          },
          {
            "step": 4,
            "component": "models.User.__init__",
            "action": "instantiates User model"
          },
          {
            "step": 5,
            "component": "models.User.save",
            "action": "persists to database"
          },
          {
            "step": 6,
            "component": "api.serializers.UserSerializer",
            "action": "serializes response"
          },
          {
            "step": 7,
            "component": "api.user_endpoints.create_user",
            "action": "returns HTTP 201"
          }
        ],
        "crossroads_traversed": ["api→models", "models→utils", "models→database"],
        "complexity": "high",
        "involves_components": ["api", "models", "utils", "database"]
      },
      {
        "path_id": "user_authentication_flow",
        "description": "User login and token generation",
        "entry_point": "myapp.api.auth_endpoints.login",
        "exit_point": "JWT token returned",
        "steps": [
          {"step": 1, "component": "api.auth.login", "action": "receives credentials"},
          {"step": 2, "component": "models.User.authenticate", "action": "validates credentials"},
          {"step": 3, "component": "utils.jwt.create_token", "action": "generates JWT"},
          {"step": 4, "component": "api.auth.login", "action": "returns token"}
        ],
        "complexity": "medium"
      }
    ],

    "data_flows": [
      {
        "flow_id": "http_request_to_database",
        "description": "HTTP request data flows from API through models to database",
        "flow_path": "HTTP request → JSON → Python dict → Validation → Model instance → Database record",
        "involves_modules": ["api", "utils", "models", "database"],
        "transformation_steps": 4,
        "potential_failures": ["validation", "database_constraint"]
      }
    ],

    "statistics": {
      "total_components": 47,
      "total_integration_points": 2847,
      "average_integration_per_component": 60.6,
      "most_integrated_module": "models.User",
      "most_integrated_module_points": 89,
      "layer_count": 4,
      "circular_dependencies": 0
    }
  }
}
```

---

## 4. Query Patterns This Enables

### Query 1: "What calls function X?"
```python
# In JSON:
tree["myapp"]["children"]["models"]["children"]["user"]["children"]["User"]["methods"]["save"]["integration_points"]["called_by"]
# Returns: [{"source": "api.create_user", "line": 78}, ...]
```

### Query 2: "What's the data flow for Y?"
```python
# In JSON:
tree["myapp"]["children"]["models"]["children"]["user"]["children"]["User"]["methods"]["save"]["data_flows"]
# Returns: Complete step-by-step flow with components and actions
```

### Query 3: "Which modules integrate with API?"
```python
# In JSON:
global_integration_map["crossroads"]
# Filter for components containing "api"
# Returns: All junctions involving API layer
```

### Query 4: "What attributes does User.save read/write?"
```python
# In JSON:
tree["myapp"]["children"]["models"]["children"]["user"]["children"]["User"]["methods"]["save"]["integration_points"]["reads_attributes"]
tree["myapp"]["children"]["models"]["children"]["user"]["children"]["User"]["methods"]["save"]["integration_points"]["writes_attributes"]
```

---

## 5. Design Principles Implemented

| Principle | Implementation |
|-----------|----------------|
| **Hierarchical** | Nested `children` dicts at every level |
| **Rich Edges** | Every connection has parameters, data flow, integration type, line number |
| **FQNs** | Every component has fully qualified name for deterministic lookup |
| **Reverse Lookups** | `called_by`, `imported_by`, `read_by`, `written_by` for instant queries |
| **Complete Integration** | EVERY import, call, attribute, inheritance tracked |
| **Optimized for LLMs** | Structure enables instant queries without file parsing |

---

## 6. Validation Checklist

Schema is correct when:
- [ ] Hierarchical tree is nested, not flat
- [ ] Every component has unique FQN and path
- [ ] All integration_points are present and rich
- [ ] Reverse lookups are complete and accurate
- [ ] crossroads identify major module boundaries
- [ ] critical_paths trace end-to-end flows
- [ ] JSON is valid and loads without errors
- [ ] Claude Code can query without file parsing

---

## 7. Edge Cases Handled

| Case | Handling |
|------|----------|
| Dynamic imports | Track as `{"target": "<dynamic>", "module_var": "name"}` |
| Star imports | Track as `{"items": "*"}` with note |
| Decorators | Track full chain with order |
| Aliases | Resolve "import X as Y" to actual FQN |
| Relative imports | Convert to absolute FQNs using file path |
| Attribute chains | Break `obj.a.b.c()` into discrete edges |

---

## 8. File Organization

- `json_schema_design.md` - THIS FILE (schema definition)
- `integration_mapper.py` - Implementation using this schema
- `integration_map.json` - Output when analyzer runs

