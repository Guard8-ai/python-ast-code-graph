# /analyze-python - Analyze Python Codebase with AST Integration Mapper

Analyze the Python codebase using AST-based integration mapping and load the analysis into your working memory. This eliminates cognitive overhead by pre-computing all component connections, crossroads, and data flows.

## What This Does

1. **Runs the integration mapper** on the Python project
2. **Generates a compact analysis** (61-70% token reduction vs verbose)
3. **Loads crossroads & critical paths** into working memory
4. **Enables instant architecture queries** without file re-parsing
5. **Frees up 60-70% of context** for actual development work

## Usage

```
/analyze-python
```

## Step-by-Step Execution

### Step 1: Generate Analysis with Integration Mapper

Run the integration mapper in context-aware (token-efficient) mode:

```bash
python src/integration_mapper/mapper.py \
  --root . \
  --output .claude/codebase_analysis.json \
  --context-aware \
  --exclude "*/tests/*,*/docs/*,*/.git/*,*/__pycache__/*,*/node_modules/*"
```

**Why context-aware mode?**
- Stores crossroads analysis instead of all 93K edges
- 61-70% smaller than verbose format
- Perfect for memory constraints
- All crossroads still included

### Step 2: Read and Verify Analysis File

```bash
cat .claude/codebase_analysis.json | head -100
```

Verify it contains:
- `v`: "2.0-compact" (correct format version)
- `meta`: Metadata with stats
- `idx`: Component ID→FQN index
- `cmp`: Flat component list
- `crd`: Crossroads (module interactions)
- `cp`: Critical paths (data flow entry points)

### Step 3: Load Analysis into Working Memory

Parse the compact analysis and memorize these key sections:

#### **A. Architecture Overview**
Read the component index (`idx`) to understand top-level structure:
- List all top-level packages
- Identify main modules
- Note their relationships

Store mental summary like:
```
Architecture:
- django: Web framework core
  ├─ http: HTTP request/response handling
  ├─ db: Database ORM
  ├─ views: View layer
  └─ urls: URL routing
```

#### **B. Crossroads Analysis**
Extract from `crd` field (module interaction points):

For each crossroad entry:
```json
{
  "id": "module_a_module_b_junction",
  "c": [42, 89],           // Component IDs
  "cnt": 247,              // Interaction count
  "crit": "h"              // Criticality: h=high, m=medium
}
```

**Memorize crossroads as:**
```
Critical Integration Points:
1. django ↔ db: 247 interactions (HIGH)
   → Main integration point for database access
2. views ↔ models: 189 interactions (HIGH)
   → View layer heavily depends on models
3. middleware ↔ http: 156 interactions (MEDIUM)
   → Request/response processing
```

#### **C. Critical Paths**
Extract from `cp` field (data flow entry points):

For each critical path:
```json
{
  "id": "path_function_name",
  "ep": 5,                 // Entry point component ID
  "cc": 88,                // Call count
  "cx": "h"                // Complexity
}
```

**Memorize critical paths as:**
```
Key Data Flow Entry Points:
1. RequestHandler.process() - Called 88 times (HIGH complexity)
   → Main entry point for request processing
2. Database.execute() - Called 67 times (HIGH complexity)
   → Central point for database operations
```

#### **D. Component Index (Sparse Lookup)**
Keep the `idx` field in memory for fast lookups:
```json
"idx": {
  "1": "django",
  "2": "django.http",
  "3": "django.db",
  ...
}
```

**Store this as a lookup table:**
- ID 42 → Component name
- ID 89 → Another component
- Use only for frequently-accessed components

### Step 4: Calculate Memory Usage

Check file size and estimate tokens:

```bash
ls -lh .claude/codebase_analysis.json
```

Estimate tokens: `file_size_bytes / 4 ≈ tokens`

**Expected results:**
- Small project (10-50 files): 5-15K tokens
- Medium project (50-200 files): 20-40K tokens
- Large project (200-1000 files): 60-80K tokens

### Step 5: Report Status and Store Insights

**Output template to provide:**

```
✅ ANALYSIS COMPLETE

📊 Codebase Statistics:
   Files analyzed: [COUNT]
   Components found: [COUNT]
   Crossroads identified: [COUNT]
   Critical paths: [COUNT]

💾 Memory Usage:
   Analysis file: [SIZE] KB
   Estimated tokens: [TOKENS]
   Context freed: ~[FREED]% for actual work

🧠 Loaded into Memory:
   ✓ Architecture overview
   ✓ Crossroads analysis ([COUNT] critical junctions)
   ✓ Critical paths ([COUNT] entry points)
   ✓ Component index (sparse lookup)

🚀 Ready for Instant Queries:
   • "What are the main integration points?"
   • "How do module A and module B connect?"
   • "What calls component X?"
   • "Where is component X defined?"
   • "What are the data flow entry points?"

💡 Tips:
   - Use /refresh-analysis after major changes
   - Analysis is accurate (AST-based, not inference)
   - Memory persists for this session
```

## Memory Management

### What's Memorized (Stays in Context)
✅ **Crossroads analysis** - Module interaction points
✅ **Critical paths** - Data flow entry points
✅ **Architecture overview** - High-level structure
✅ **Sparse index** - Frequently-accessed FQNs

### What's Not Memorized (On-Demand)
📄 Full component tree - Use index for specific lookups
📄 All FQNs - Only cache what you need
📄 Raw edges - Crossroads provide sufficient detail

### Lazy Loading Pattern
When user asks about a component not in memory:
1. Look up component ID in cached index
2. If needed, load full details from `.claude/codebase_analysis.json`
3. Cache the result for future queries
4. Keep memory usage bounded

## Error Handling

### If analysis file doesn't exist:
```
❌ No analysis found at `.claude/codebase_analysis.json`

Solution:
1. Run the integration mapper command from Step 1
2. Or re-run: /analyze-python

⏱️  This typically takes:
   - Small projects: 1-5 seconds
   - Medium projects: 5-15 seconds
   - Large projects: 15-45 seconds
```

### If analysis is corrupted or invalid:
```
❌ Analysis file is invalid or corrupted

Troubleshooting:
1. Delete the corrupted file:
   rm .claude/codebase_analysis.json
2. Re-run: /analyze-python
3. If error persists, check Python environment:
   python src/integration_mapper/mapper.py --help
```

### If token count is too high:
```
⚠️  Analysis is large ([TOKENS] tokens)

Options:
1. Exclude more directories:
   --exclude "*/tests/*,*/docs/*,*/build/*,*/dist/*"
2. Focus on specific module:
   --root ./src/specific_module
3. Use on-demand queries instead of memorizing everything
```

## Query Examples After Loading Analysis

Once analysis is memorized, you can instantly answer questions like:

**"What are the main integration points in this codebase?"**
→ Return memorized crossroads (from `crd` field)

**"How does the API layer connect to the database?"**
→ Check crossroads for api ↔ database interactions

**"What calls the User.save() method?"**
→ Look up User.save in component index, check its crossroads

**"What are the data flow entry points?"**
→ Return memorized critical paths (from `cp` field)

**"Which modules have the most interactions?"**
→ Sort crossroads by `cnt` field, return top 5-10

**"Is there a circular dependency between A and B?"**
→ Check crossroads for both A→B and B→A connections

## Performance Impact

**Before Analysis:**
- Every question requires file parsing
- Time per query: 10-30 seconds
- Context: 100% available but underutilized

**After Analysis (in memory):**
- Instant answers from memorized crossroads
- Time per query: <1 second
- Context: 30-40% for analysis, 60-70% for work
- **Speedup: 100-1000x faster** 🚀

## Refresh When Needed

After major code changes, use `/refresh-analysis` to update the analysis:

```
/refresh-analysis
```

This will:
- Re-run the mapper
- Compare with previous analysis
- Report what changed
- Update working memory

## Storage & Gitignore

The analysis file is stored at `.claude/codebase_analysis.json` and should be added to `.gitignore`:

```
# .gitignore
.claude/codebase_analysis.json
```

This keeps the analysis local and fresh for each developer.

## Summary

✅ **One command to transform your development workflow**

- **Instant answers** to architecture questions
- **100-1000x faster** than file parsing
- **60-70% context savings** vs verbose analysis
- **AST-accurate** (not inference-based)
- **Easy to refresh** after changes

**Result:** Claude Code becomes an architecture-aware assistant that never forgets your codebase structure!
