# /refresh-analysis - Refresh Python Codebase Analysis

Refresh the codebase analysis to reflect recent code changes. Use this after major refactoring, adding new modules, or periodically to keep the analysis current.

## What This Does

1. **Re-runs the integration mapper** to capture current state
2. **Compares with previous analysis** to identify changes
3. **Reports what changed:**
   - New files added
   - Files removed
   - New components discovered
   - New crossroads identified
   - Critical paths updated
4. **Updates working memory** with new insights
5. **Keeps analysis fresh** and accurate

## Usage

```
/refresh-analysis
```

## When to Use

- ✅ After adding new modules
- ✅ After major refactoring
- ✅ After merging feature branches
- ✅ Periodically (every few days for active projects)
- ✅ Before important architecture queries

## Step-by-Step Execution

### Step 1: Check if Previous Analysis Exists

```bash
test -f .claude/codebase_analysis.json && echo "Previous analysis found" || echo "No previous analysis"
```

**If no previous analysis:**
```
ℹ️  No previous analysis found.
Run /analyze-python first to generate initial analysis.
```

**If previous analysis exists, proceed to Step 2.**

### Step 2: Backup Previous Analysis

Create a backup before regenerating:

```bash
cp .claude/codebase_analysis.json .claude/codebase_analysis.previous.json
```

This allows comparison between old and new versions.

### Step 3: Generate New Analysis

Run the integration mapper with same parameters as before:

```bash
python src/integration_mapper/mapper.py \
  --root . \
  --output .claude/codebase_analysis.json \
  --context-aware \
  --exclude "*/tests/*,*/docs/*,*/.git/*,*/__pycache__/*,*/node_modules/*"
```

### Step 4: Compare Analyses

Read both files and identify differences:

```bash
# Check file sizes (should be similar or grow slightly)
ls -lh .claude/codebase_analysis.{,previous.}json

# Quick content comparison
head -50 .claude/codebase_analysis.json
head -50 .claude/codebase_analysis.previous.json
```

### Step 5: Extract Change Summary

Parse both analysis files and calculate differences:

#### **From metadata comparison:**

**Previous (`previous.json`):**
```
meta: {
  "c": 12185,              // Component count
  "r": 93355,              // Relationship count (edges)
  "ts": "2025-10-16T...",  // Timestamp
  "fc": 899,               // Files analyzed
  "cc": 12185              // Components found
}
```

**Current (`.json`):**
```
meta: {
  "c": 12200,              // +15 new components
  "r": 93500,              // +145 new edges
  "ts": "2025-10-17T...",  // Updated timestamp
  "fc": 905,               // +6 new files
  "cc": 12200              // Updated count
}
```

#### **Calculate changes:**
```
Component changes: 12200 - 12185 = +15 components
Edge changes: 93500 - 93355 = +145 edges
File changes: 905 - 899 = +6 files
Crossroad changes: Compare crd array sizes
Critical path changes: Compare cp array sizes
```

### Step 6: Identify Major Changes

Compare crossroads (from `crd` field):

**Previous crossroads:**
```json
"crd": [
  {"id": "django_db_junction", "c": [42, 89], "cnt": 247, "crit": "h"},
  {"id": "views_models_junction", "c": [45, 67], "cnt": 189, "crit": "h"}
]
```

**Current crossroads:**
```json
"crd": [
  {"id": "django_db_junction", "c": [42, 89], "cnt": 267, "crit": "h"},     // +20 interactions
  {"id": "views_models_junction", "c": [45, 67], "cnt": 189, "crit": "h"},
  {"id": "cache_services_junction", "c": [103, 145], "cnt": 156, "crit": "m"} // NEW
]
```

**Identify:**
- Existing crossroads with changed interaction counts
- New crossroads (potential new integration points)
- Removed crossroads (decoupling)

### Step 7: Generate Change Report

Output a structured change summary:

```
✅ ANALYSIS REFRESHED

📊 Changes Since Last Analysis:
   Files: 899 → 905 (+6 new files)
   Components: 12,185 → 12,200 (+15 new components)
   Edges: 93,355 → 93,500 (+145 new edges)
   Time elapsed: 23 seconds

🔗 Crossroads Changes:
   Existing crossroads updated:
   • django ↔ db: 247 → 267 interactions (+20)
     Reason: More database calls in new code

   New crossroads discovered:
   • cache ↔ services: 156 interactions (MEDIUM)
     Location: New caching layer added

   Crossroads removed: None

📍 Critical Paths Updated:
   Previous: 5 critical paths
   Current: 6 critical paths

   New entry point:
   • CacheService.get_or_fetch() - Called 64 times (MEDIUM)
     Added by: New caching infrastructure

⚠️  Notable Changes:
   • Request ↔ Database interactions increased by 20
     Suggest reviewing database query optimization
   • New cache layer reduces load on models module
     Positive: Improves performance architecture

🧠 Updated in Memory:
   ✓ Architecture updated (new cache layer)
   ✓ Crossroads refreshed (6 total)
   ✓ Critical paths updated (6 total)
   ✓ Component index expanded (12,200 components)

💡 Recommendations:
   1. Review database interaction increase
   2. Test new cache layer under load
   3. Run /analyze-python on feature branches before merge
```

### Step 8: Update Working Memory

Update the memorized information with new data:

**New or changed sections to memorize:**
- ✅ Updated architecture (if new top-level packages)
- ✅ New crossroads entries
- ✅ Changed interaction counts for existing crossroads
- ✅ New critical paths
- ✅ Removed/changed integration points

**Keep unchanged:**
- Old crossroads data (unless counts changed)
- Stable critical paths
- Base architecture

## Cleanup

### Remove backup (optional)

```bash
rm .claude/codebase_analysis.previous.json
```

Or keep it for historical comparison:
```bash
mv .claude/codebase_analysis.previous.json \
   .claude/codebase_analysis.backup.$(date +%Y%m%d_%H%M%S).json
```

## Error Handling

### If new analysis fails:

```
❌ Failed to generate new analysis

Troubleshooting:
1. Check if integration_mapper.py exists:
   ls src/integration_mapper/mapper.py

2. Try running directly:
   python src/integration_mapper/mapper.py --help

3. Check for syntax errors in changed files:
   python -m py_compile changed_file.py

4. If persistent, restore previous analysis:
   mv .claude/codebase_analysis.previous.json \
      .claude/codebase_analysis.json
```

### If comparison fails:

```
⚠️  Could not compare old and new analyses

Possible reasons:
1. Previous analysis in different format (update to context-aware)
2. Corrupted backup file
3. First refresh after moving to new format

Action: Just use new analysis (previous backup not needed)
```

## Comparison Scenarios

### Scenario 1: Small Refactoring
```
Changes: 1-5 files modified
Result: Similar analysis size, minor stat changes
Action: Continue with updated analysis
```

### Scenario 2: Feature Branch Merge
```
Changes: 10-50 files added, new crossroads discovered
Result: Analysis size grows slightly
Action: Review new crossroads and update memory
```

### Scenario 3: Major Restructuring
```
Changes: 50+ files reorganized, architecture changes
Result: Analysis size changes significantly
Action: Review architecture changes, update mental model completely
```

### Scenario 4: Large Codebase
```
Changes: After working on 900+ file project for a week
Result: 5-20% growth in stats
Action: Refresh weekly to stay current
```

## Integration with Development

### Typical Workflow

```
# Start session
/analyze-python              # Load initial analysis

# Work for a while...
# Add features, refactor code

# Before committing
/refresh-analysis            # Check what changed

# Get instant answers
"What are the new integration points I added?"
"Did I introduce any circular dependencies?"
"How does my new module fit into the architecture?"

# Commit with confidence
git commit -m "Add new caching layer with improved crossroads"
```

### In CI/CD Pipeline (Optional)

```bash
# Generate reference analysis
python src/integration_mapper/mapper.py --root . --output reference.json --context-aware

# After changes, refresh and diff
python src/integration_mapper/mapper.py --root . --output current.json --context-aware
diff reference.json current.json
```

## Performance

**Refresh time depends on:**
- Project size (100 files: 2-5s, 900 files: 20-30s)
- Number of changes (more changes = more work)
- System performance

**Memory impact:**
- Refreshed analysis replaces old one (no accumulation)
- Memory stays bounded at same level as initial analysis

## Advanced: Incremental Updates

For very large projects, consider incremental analysis:

```bash
# Analyze only changed files (if supported)
git diff --name-only HEAD~1 | grep '\.py$' | \
  xargs python src/integration_mapper/mapper.py --files
```

This would need custom flag support in mapper.

## Summary

✅ **Keep your analysis fresh and accurate**

- **Detect architectural changes** as they happen
- **Update memory incrementally** (no re-learning needed)
- **Compare old vs new** to understand impact
- **Stay current** without manual tracking

**Run `/refresh-analysis` regularly to maintain architectural awareness!**
