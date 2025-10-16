# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **specification and planning repository** for a Python AST analyzer called **Integration Mapper**. The project is NOT a working codebase yet—it's a detailed specification designed to guide implementation of a tool that generates hierarchical integration maps of Python codebases.

**Core Mission:** Build `integration_mapper.py`, a stdlib-only Python script that analyzes any Python codebase and outputs a single JSON file showing EVERY connection, crossroad, and data flow between components. This enables Claude Code to answer architecture questions instantly without parsing files.

## Why This Project Exists

Claude Code wastes cognitive cycles reconstructing codebase structure and integration patterns. The Integration Mapper pre-computes this knowledge in a hierarchical JSON file, eliminating the need for file parsing and inference when working with codebases.

## Key Concepts

### Integration-First Philosophy
The value isn't in listing components—it's in mapping HOW components integrate. Every edge in the output graph must answer "HOW do these components connect?" with full context (parameters, data flow, purpose).

### Three-Phase Architecture
1. **Discovery & Hierarchy Building**: Traverse filesystem, build nested tree structure, assign FQNs
2. **Integration Point Extraction**: Map imports, calls, attributes, inheritance with rich metadata
3. **Flow & Crossroad Analysis**: Trace data flows, detect module boundaries, identify critical paths

### Core Output Structure
- Hierarchical tree (NOT flat list): `package → module → class → method`
- Rich integration metadata at every node (parameters, data flow, usage counts)
- Global integration map section with crossroads and critical paths
- Fully qualified names (FQNs) for deterministic lookups
- Reverse lookups (`called_by`, `imported_by`, `read_by`, `written_by`)

## Repository Structure

```
code-graph/
├── documentation/
│   ├── codebase_vision.md          # Problem statement and vision
│   ├── philosophical_alignment.md  # Integration-first philosophy
│   ├── implementation_instructions.md  # Three-phase detailed architecture
│   ├── success_criteria.md         # Validation tests and metrics
│   ├── P1_refined_prompt.md        # Final refined prompt for implementation
│   └── developer-handoff0.md       # Complete technical handoff
├── reference/
│   ├── integration_schema.json     # Output JSON schema examples
│   └── followup_prompts.md         # Iterative refinement prompts
├── project_management/
│   ├── AI_AGENT_SETUP_NOTIFICATION.md  # TaskGuard integration notes
│   ├── AGENTIC_AI_TASKGUARD_GUIDE.md   # TaskGuard workflow
│   └── .taskguard/                     # TaskGuard configuration
├── tasks/                          # TaskGuard task files (organized by area)
└── CLAUDE.md                       # This file
```

## Development Workflow with TaskGuard

This project uses **TaskGuard** for task management and tracking. Use these commands consistently:

```bash
# Initialize and check state
taskguard init
taskguard list
taskguard validate

# Create tasks (one per area to avoid ID conflicts)
taskguard create --title "Task name" --area backend --priority high

# Update task status
taskguard update status <task-id> doing      # When starting work
taskguard update status <task-id> done       # When complete
taskguard update dependencies <task-id> "dep1,dep2"  # Set dependencies

# Track progress
taskguard list items <task-id>
taskguard task update <task-id> <item-index> done
```

**Available areas:** setup, docs, backend, api, frontend, auth, data, testing, integration, deployment

**Key principle:** Create dependency chains. Foundation tasks (setup, docs) have no dependencies. Implementation tasks depend on foundation. Validation tasks depend on implementation.

## Commands for Development

Since this is a specification repository, there are no build or test commands yet. The focus is on:

### Documentation Reading
```bash
# Read specification documents in order
cat codebase_vision.md               # Understand the problem
cat philosophical_alignment.md       # Understand the approach
cat implementation_instructions.md   # Understand the architecture
cat success_criteria.md              # Understand success metrics
cat P1_refined_prompt.md            # Read final refined prompt
```

### Validation
```bash
# Check JSON schema validity
python -m json.tool integration_schema.json > /dev/null
```

### TaskGuard Management
All work should flow through TaskGuard to maintain consistency with the project's agentic workflow.

## High-Level Architecture

### Phase 1: Hierarchical Structure Building (2-3 hours)
- Set up CLI with `--root`, `--output`, `--exclude` flags
- Implement filesystem discovery (find all `.py` files)
- Build `HierarchyBuilder` AST visitor to traverse code structure
- Create nested JSON tree structure with FQNs
- **Success:** Tree reflects actual folder/file structure with all components

### Phase 2: Rich Integration Context (3-4 hours)
- Enhance `IntegrationExtractor` for calls with parameters
- Add usage counting for imports
- Distinguish read/write for attribute access
- Build reverse lookups (`called_by`, `imported_by`, `read_by`, `written_by`)
- **Success:** Every edge has metadata (parameters, data flow, integration type)

### Phase 3: Flow & Crossroad Analysis (2-3 hours)
- Implement `FlowAnalyzer` to trace data flows
- Detect module boundary crossroads
- Identify critical paths
- Generate `global_integration_map` section
- **Success:** Flows are complete, crossroads identified, global map populated

**Total estimated time:** 8-12 hours focused development across 3 iterations

## Critical Requirements

When implementing Integration Mapper, these are non-negotiable:

### 1. Hierarchical Output (NOT Flat)
```json
✅ CORRECT:
{
  "myapp": {
    "children": {
      "models": {
        "children": {
          "user": { ... }
        }
      }
    }
  }
}

❌ WRONG:
{
  "nodes": [
    { "id": "myapp", ... },
    { "id": "myapp.models", ... },
    { "id": "myapp.models.user", ... }
  ]
}
```

### 2. Rich Integration Edges
Every edge must include context. NEVER output bare `{"source": "A", "target": "B"}` edges.

```json
✅ CORRECT:
{
  "source": "api.create_user",
  "target": "User.save",
  "line": 42,
  "args": [
    {"name": "force_insert", "value": "True", "type": "bool"}
  ],
  "data_flow": "request_data → User() → user.save() → database",
  "integration_type": "api_to_model_call",
  "side_effects": ["database_write"]
}

❌ WRONG:
{
  "source": "api.create_user",
  "target": "User.save",
  "type": "call"
}
```

### 3. Fully Qualified Names (FQNs)
Every component must have a deterministic FQN that reflects its location in the codebase. Use this for lookups and to avoid ambiguity.

### 4. Alias Resolution
Track and resolve all import aliases (`import X as Y`), relative imports (`.module`, `..parent`), and dynamic imports. Never output unresolved aliases in the final JSON.

### 5. Reverse Lookups
For every relationship (call, import, attribute access, inheritance), maintain reverse references so you can instantly answer "what uses this component?"

## Success Criteria

You've successfully implemented Integration Mapper when:

### Structural Completeness
- [ ] JSON loads without errors
- [ ] Tree is hierarchical with nested `children` dicts
- [ ] Every component has unique FQN as `id`
- [ ] Tree structure mirrors actual folder structure

### Integration Richness
- [ ] EVERY import relationship captured with specific items and usage counts
- [ ] EVERY function call mapped with parameters, data flow, line number
- [ ] EVERY class inheritance chain tracked with overridden methods
- [ ] EVERY attribute access recorded with read/write distinction

### LLM Usability (The Real Test)
- [ ] Claude Code can answer "what calls function X?" by reading JSON (no file parsing)
- [ ] Claude Code can trace data flows end-to-end
- [ ] Claude Code can identify module boundary crossroads
- [ ] Developer can understand a new 500-file codebase in 10 minutes using the map

### Performance
- [ ] 100 files analyzed in <15 seconds
- [ ] 500 files analyzed in <30 seconds
- [ ] JSON output <10MB for 1000 files
- [ ] Memory usage <1GB during analysis

## Key Files to Reference

1. **codebase_vision.md** - Read first for problem statement and philosophy
2. **philosophical_alignment.md** - Understand the integration-first approach
3. **implementation_instructions.md** - Detailed three-phase architecture
4. **integration_schema.json** - Example JSON output structures
5. **success_criteria.md** - Validation tests and metrics
6. **P1_refined_prompt.md** - Complete refined prompt ready for implementation
7. **developer-handoff0.md** - Comprehensive technical handoff with all details

## Common Pitfalls to Avoid

### ❌ Flat Output
Don't output node lists. Use nested `children` dicts at every level to maintain hierarchy.

### ❌ Shallow Edges
Don't output edges without context. Every edge must have parameters, data flow, integration type, and line numbers.

### ❌ Unresolved Aliases
Don't leave "json" or "pd" in output. Always resolve aliases to actual module names.

### ❌ Missing Reverse Lookups
Don't make it hard to find what uses a component. Maintain `called_by`, `imported_by`, `read_by`, `written_by` lists.

### ❌ Incomplete Data Flows
Don't trace flows with gaps. Complete paths from entry point to exit point.

## TaskGuard Integration Strategy

When working on this project, use TaskGuard to structure work:

### Foundation Phase
- `setup-001`: Verify specification clarity
- `docs-001`: Document schema and architecture decisions

### Implementation Phase
- `backend-001`: Build hierarchy structure
- `backend-002`: Extract integration points
- `backend-003`: Analyze flows and crossroads
- `api-001`: Design CLI interface

### Validation Phase
- `testing-001`: Create test cases
- `testing-002`: Run validation tests
- `integration-001`: End-to-end integration testing

Each task should have clear dependencies flowing from foundation → implementation → validation.

## Notes for Claude Code Instances

1. **This is a specification repository**: There's no working code to run yet. Your job is to implement `integration_mapper.py` following the specifications in the documents.

2. **Use integration-first thinking**: The value is in HOW components connect, not what they are. Every design decision should prioritize rich integration context.

3. **Leverage TaskGuard**: Use it consistently to track progress and maintain discipline across implementation iterations.

4. **Validate constantly**: After each phase, validate against the success criteria. Don't move to the next phase until the current one is solid.

5. **Test on small codebases first**: Implement on a 5-10 file test project before scaling to large codebases.

6. **Keep dependencies minimal**: Stay stdlib-only. No external packages. Maximum portability.

---

**Good luck building the Integration Mapper!** 🚀 This tool will transform how Claude Code (and developers) understand and work with codebases. The specifications are comprehensive—follow them, validate frequently, and deliver a working integration mapper that enables instant architectural understanding.
