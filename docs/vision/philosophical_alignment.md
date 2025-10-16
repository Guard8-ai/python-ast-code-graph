# PHILOSOPHICAL ALIGNMENT

## Core Philosophy: Integration-First Thinking

**Problem-First Origin:**
Claude Code wastes time reconstructing the connective tissue of codebases. Every refactor, every new feature, every bug fix requires understanding "what connects to what?" Without a pre-computed integration map, developers and AI assistants burn cognitive cycles on the same discovery work repeatedly.

**Deep Principle:**
> "The VALUE of a codebase isn't in its components—it's in how components INTEGRATE."

A function alone is trivial. A function that's called by 15 other functions across 8 modules is an architectural crossroad that requires careful handling. Map the crossroads, not just the streets.

## Decision Framework: What Gets Mapped?

### ✅ IN SCOPE (Critical Integration Points)
- **Function calls** with parameters, return values, data flow
- **Attribute access** (read/write) with usage patterns
- **Import relationships** with what specifically gets used
- **Inheritance chains** with method overrides
- **Data flows** from entry point to exit point
- **Crossroads** where multiple modules intersect
- **Junction points** between architectural layers (API→Models→DB)

### ❌ OUT OF SCOPE (Doesn't Show Integration)
- Abstract syntax tree dumps (too low-level)
- Line-by-line code analysis (not architectural)
- Performance profiling (different concern)
- Test coverage metrics (separate tool)
- Documentation generation (not integration mapping)

## Architectural Principles

### 1. Hierarchy Over Flatness
**Why:** Developers think in trees, not graphs. "This package contains modules which contain classes which have methods."

**Not This:** Flat list of 2000 functions
**This:** Nested tree showing containment and integration at each level

### 2. Rich Context at Integration Points
**Why:** "Function X calls Function Y" is useless. "Function X passes user_id to Function Y which then queries the database" is actionable.

**Not This:** Edge without metadata
**This:** Edge with parameters, data flow, integration type, purpose

### 3. Flow Over Static Structure
**Why:** Code is dynamic. Data flows through the system. Control passes between components. Map the FLOW, not just the structure.

**Not This:** "Class A has method B"
**This:** "Class A method B receives request data, validates via Utils.validate(), saves to DB, returns serialized response to API layer"

### 4. Crossroads Are Critical
**Why:** Most bugs happen at integration boundaries. Most refactoring affects crossroads. Map where components MEET, not just where they exist.

**Focus On:**
- Module boundary crossings (api→models)
- Layer transitions (controller→service→repository)
- State mutations (who writes to what)
- Dependency junctions (N things depend on M things)

## Developer Sovereignty Principles

### Your Code, Your Decisions
The analyzer maps integration points—YOU decide what to do with that information. No "best practices" enforced. No architecture judgments. Pure data about how your codebase connects.

### Simple Tool, Powerful Output
Stdlib-only Python script. No framework. No dependencies. No magic. Reads your code, outputs hierarchical JSON. What you do with it is YOUR choice.

### Quick and Functional
Ship a working integration map in one iteration. Refine based on real usage. Don't build the perfect analyzer—build the useful one.

## Anti-Patterns (What This Is NOT)

❌ **Not a code quality tool** - doesn't judge your architecture
❌ **Not a linter** - doesn't enforce style
❌ **Not a test framework** - doesn't validate correctness
❌ **Not a refactoring engine** - doesn't modify code
❌ **Not an optimization tool** - doesn't measure performance

✅ **IS an integration microscope** - reveals how components connect
✅ **IS a flow mapper** - shows data and control paths
✅ **IS a crossroad catalog** - identifies architectural junctions
✅ **IS an LLM context generator** - gives Claude Code perfect memory

## Success Philosophy

**Metric:** Can Claude Code answer integration questions WITHOUT parsing files?
- "What calls this function?" → Read graph, instant answer
- "What's the data flow for user login?" → Read graph, see complete path
- "Where do API and models integrate?" → Read crossroads section

**Metric:** Can a developer understand a new codebase in 10 minutes?
- Read hierarchy tree → see package structure
- Read crossroads → see major integration points
- Read critical paths → see key flows

**Metric:** Does refactoring become predictable?
- Change function X → graph shows 12 callers to update
- Change data model → graph shows complete flow to audit
- Delete module → graph shows all dependent modules

## The "Why" Behind Rich Data

**Shallow:** `{"source": "funcA", "target": "funcB", "type": "call"}`
**Problem:** Tells you WHAT but not HOW or WHY

**Rich:** 
```json
{
  "source": "api.create_user",
  "target": "models.User.save",
  "type": "call",
  "args": ["username", "email"],
  "data_flow": "request_data -> validation -> persistence",
  "integration_type": "api_to_model",
  "context": "User creation endpoint",
  "side_effects": ["database_write", "cache_invalidation"]
}
```
**Value:** Shows HOW components integrate, enabling confident changes

## Naming Philosophy

Names should reveal integration semantics:
- `integration_points` not `edges` (shows purpose)
- `crossroads` not `junctions` (evokes intersection)
- `data_flows` not `traces` (shows movement)
- `called_by` not `reverse_edges` (shows relationship)

Good names make the graph self-documenting for LLMs and humans.
