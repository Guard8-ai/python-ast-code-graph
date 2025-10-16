#!/usr/bin/env python3
"""
Validate JSON schema design by creating and testing example outputs.
"""

import json
import sys


def create_example_json():
    """Create an example JSON following the schema."""
    example = {
        "metadata": {
            "total_integration_points": 47,
            "total_crossroads": 3,
            "analysis_timestamp": "2025-10-16T14:30:00Z",
            "python_version": "3.8+",
            "files_analyzed": 2,
            "packages": 1,
            "modules": 2,
            "classes": 1,
            "functions": 2
        },
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
                                "source": "typing",
                                "items": ["Dict", "Any"],
                                "usage_count": 3,
                                "line": 1,
                                "integration_type": "stdlib_import"
                            }
                        ],
                        "children": {
                            "User": {
                                "type": "class",
                                "line_range": [5, 25],
                                "inherits": [],
                                "attributes": {
                                    "name": {
                                        "type": "str",
                                        "line": 6,
                                        "read_by": ["get_name"],
                                        "written_by": ["__init__"]
                                    }
                                },
                                "methods": {
                                    "save": {
                                        "type": "method",
                                        "line_range": [15, 20],
                                        "parameters": [
                                            {"name": "self", "type": "User"}
                                        ],
                                        "return_type": "None",
                                        "integration_points": {
                                            "calls": [
                                                {
                                                    "target": "dict",
                                                    "target_fqn": "builtins.dict",
                                                    "line": 16,
                                                    "args": [],
                                                    "return_captured": True,
                                                    "return_var": "data",
                                                    "data_flow": "create user data dict",
                                                    "integration_type": "builtin_call"
                                                }
                                            ],
                                            "called_by": [
                                                {
                                                    "source": "myapp.api.create_user",
                                                    "source_fqn": "myapp.api.create_user",
                                                    "line": 30,
                                                    "context": "API endpoint"
                                                }
                                            ],
                                            "reads_attributes": [
                                                {"attr": "self.name", "line": 17}
                                            ],
                                            "writes_attributes": []
                                        },
                                        "data_flows": []
                                    }
                                },
                                "class_integration_summary": {
                                    "total_integration_points": 12,
                                    "integration_types": {
                                        "calls": 3,
                                        "called_by": 2,
                                        "attribute_reads": 4,
                                        "attribute_writes": 1
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
                    "crossroad_id": "api_to_models",
                    "type": "module_boundary",
                    "components": ["myapp.api", "myapp.models"],
                    "integration_patterns": ["API calls model.save()"],
                    "integration_count": 5,
                    "criticality": "high"
                }
            ],
            "critical_paths": [
                {
                    "path_id": "user_save_path",
                    "entry_point": "myapp.api.create_user",
                    "exit_point": "models.User saved",
                    "steps": [
                        {"step": 1, "component": "api.create_user", "action": "receive request"},
                        {"step": 2, "component": "models.User.save", "action": "save user"}
                    ],
                    "complexity": "low"
                }
            ],
            "data_flows": [],
            "statistics": {
                "total_components": 2,
                "total_integration_points": 47,
                "circular_dependencies": 0
            }
        }
    }
    return example


def validate_structure(json_obj):
    """Validate JSON structure follows schema."""
    errors = []

    # Check top-level sections
    required_sections = ["metadata", "codebase_tree", "global_integration_map"]
    for section in required_sections:
        if section not in json_obj:
            errors.append(f"Missing top-level section: {section}")

    # Check metadata
    metadata = json_obj.get("metadata", {})
    required_metadata = ["total_integration_points", "analysis_timestamp"]
    for field in required_metadata:
        if field not in metadata:
            errors.append(f"Missing metadata field: {field}")

    # Check tree is hierarchical (not flat)
    tree = json_obj.get("codebase_tree", {})
    for package_name, package_data in tree.items():
        if "children" not in package_data:
            errors.append(f"Package '{package_name}' has no 'children' key")
        if "type" not in package_data:
            errors.append(f"Package '{package_name}' has no 'type' field")

    # Check crossroads exist
    global_map = json_obj.get("global_integration_map", {})
    if "crossroads" not in global_map:
        errors.append("Missing global_integration_map.crossroads")
    if "critical_paths" not in global_map:
        errors.append("Missing global_integration_map.critical_paths")

    return errors


def query_example(json_obj):
    """Test typical queries on the example JSON."""
    queries_passed = 0

    # Query 1: Navigate hierarchy
    try:
        user_class = (
            json_obj["codebase_tree"]["myapp"]["children"]["models"]
            ["children"]["User"]
        )
        assert user_class["type"] == "class"
        print("✅ Query 1: Navigate to User class via hierarchy")
        queries_passed += 1
    except (KeyError, AssertionError) as e:
        print(f"❌ Query 1 failed: {e}")

    # Query 2: Find what calls User.save
    try:
        called_by = (
            json_obj["codebase_tree"]["myapp"]["children"]["models"]
            ["children"]["User"]["methods"]["save"]["integration_points"]["called_by"]
        )
        assert len(called_by) > 0
        assert called_by[0]["source"] == "myapp.api.create_user"
        print("✅ Query 2: Find callers of User.save")
        queries_passed += 1
    except (KeyError, AssertionError) as e:
        print(f"❌ Query 2 failed: {e}")

    # Query 3: Find crossroads
    try:
        crossroads = json_obj["global_integration_map"]["crossroads"]
        assert len(crossroads) > 0
        assert crossroads[0]["type"] == "module_boundary"
        print("✅ Query 3: Find module boundary crossroads")
        queries_passed += 1
    except (KeyError, AssertionError) as e:
        print(f"❌ Query 3 failed: {e}")

    # Query 4: Find read/write attributes
    try:
        reads = (
            json_obj["codebase_tree"]["myapp"]["children"]["models"]
            ["children"]["User"]["methods"]["save"]["integration_points"]["reads_attributes"]
        )
        assert len(reads) > 0
        print("✅ Query 4: Find attribute reads in method")
        queries_passed += 1
    except (KeyError, AssertionError) as e:
        print(f"❌ Query 4 failed: {e}")

    return queries_passed


def main():
    """Run validation tests."""
    print("🔍 JSON SCHEMA VALIDATION")
    print("=" * 60)

    # Create example
    example_json = create_example_json()

    # Validate JSON is parseable
    try:
        json_str = json.dumps(example_json)
        json.loads(json_str)
        print("✅ Valid JSON structure")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return 1

    # Validate schema
    print("\n📋 Schema Validation:")
    errors = validate_structure(example_json)
    if not errors:
        print("✅ Schema structure complete")
    else:
        for error in errors:
            print(f"❌ {error}")
        return 1

    # Test queries
    print("\n🔍 Query Testing:")
    queries_passed = query_example(example_json)
    print(f"✅ {queries_passed}/4 queries passed")

    if queries_passed < 4:
        return 1

    print("\n" + "=" * 60)
    print("✅ JSON SCHEMA VALIDATION PASSED")
    print("\nSchema enables:")
    print("  • Hierarchical navigation (packages → modules → classes → methods)")
    print("  • Instant reverse lookups (called_by, imported_by, etc.)")
    print("  • Rich edge metadata (parameters, data flow, integration type)")
    print("  • Crossroad and critical path discovery")
    print("  • Zero file parsing needed for architecture queries\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())
