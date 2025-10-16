# SUCCESS CRITERIA

## Immediate Success (Iteration 1)

### ✅ Structural Correctness
- [ ] JSON loads without errors
- [ ] Hierarchical tree structure (nested `children`, not flat)
- [ ] Every module, class, function has unique FQN as `id`
- [ ] Tree reflects actual folder/file structure of codebase
- [ ] Each node has required fields: `type`, `path`/`line_range`, `integration_points`

### ✅ Integration Completeness
- [ ] EVERY import relationship captured with specific items
- [ ] EVERY function call mapped with source line
- [ ] EVERY class inheritance chain tracked
- [ ] EVERY attribute access (read/write) recorded
- [ ] No "orphan" components (everything integrated somewhere)

### ✅ LLM Usability Test
**Can Claude Code answer these WITHOUT parsing code?**
- [ ] "Show me all functions that call `User.save`" → Read `User.save.integration_points.called_by`
- [ ] "What does `create_user` import?" → Read `create_user.imports`
- [ ] "What's the hierarchy of `myapp.models`?" → Traverse `tree.myapp.children.models.children`
- [ ] "Which functions write to `User.email`?" → Read `User.email.written_by`

## Integration Depth Success (Iteration 2)

### ✅ Rich Context at Edges
- [ ] Call edges include: parameters passed, return value captured, data flow direction
- [ ] Import edges include: usage count, which specific items used
- [ ] Attribute edges include: read vs write, purpose/context
- [ ] Inheritance edges include: overridden methods listed

### ✅ Crossroad Detection
- [ ] `global_integration_map.crossroads` section exists
- [ ] Major module boundaries identified (api↔models, models↔database)
- [ ] Multi-component junctions highlighted
- [ ] Integration pattern summaries at each crossroad

### ✅ Data Flow Visibility
- [ ] Entry-to-exit flows mapped for key functions
- [ ] Intermediate steps shown with component + action
- [ ] Side effects noted (database writes, cache invalidation)
- [ ] Critical paths marked

## Developer Experience Success

### ✅ 10-Minute Codebase Understanding
**Give fresh developer the JSON, can they answer:**
- [ ] "What are the main packages?" → Read top-level `codebase_tree`
- [ ] "Where does API talk to database?" → Read crossroads
- [ ] "What's the user creation flow?" → Read data_flows
- [ ] "Which modules have highest integration complexity?" → Count integration_points

### ✅ Zero Cognitive Overhead for Claude Code
- [ ] No file parsing needed to answer architecture questions
- [ ] No inference needed ("probably calls X" → "definitely calls X at line 42")
- [ ] No ambiguity (aliases resolved, FQNs explicit)
- [ ] Instant reverse lookups (what calls this, what imports this)

## Quantitative Metrics

### Coverage Metrics
```
✅ Module Coverage: 100% of .py files mapped
✅ Class Coverage: 100% of classes in tree
✅ Function Coverage: 100% of functions/methods in tree
✅ Import Coverage: 100% of import statements captured
✅ Call Coverage: >95% of function calls mapped (exclude dynamic)
```

### Integration Richness
```
✅ Calls with parameters: >80%
✅ Imports with usage counts: >90%
✅ Attributes with read/write distinction: 100%
✅ Major crossroads identified: >5 (for medium codebase)
✅ Critical paths mapped: >3
```

### Performance
```
✅ Analysis speed: <30 seconds for 500 files
✅ JSON file size: <10MB for 1000 files
✅ Memory usage: <1GB during analysis
```

## Failure Criteria (Red Flags)

### ❌ Structural Failures
- Flat list instead of hierarchy
- Missing components (functions/classes not in tree)
- Duplicate FQNs
- Broken parent-child relationships

### ❌ Integration Failures
- Call edges without line numbers
- Import edges without specific items
- Generic "calls X" without context
- No crossroads identified
- No data flows mapped

### ❌ Usability Failures
- Claude Code must parse files to answer questions
- Developer can't navigate tree intuitively
- Aliases unresolved (showing "json" instead of actual module)
- FQNs don't match actual code structure

## Validation Tests

### Test 1: Reverse Lookup Accuracy
```
Pick 10 random functions
For each: verify "called_by" list is complete
Result: All callers found, zero false positives
```

### Test 2: Data Flow Completeness
```
Trace user login flow end-to-end
Verify: every step in path is in the graph
Result: Complete path with no gaps
```

### Test 3: Crossroad Identification
```
List major module boundaries in codebase
Check: graph identifies same boundaries
Result: All critical junctions detected
```

### Test 4: LLM Query Speed
```
Ask Claude Code 10 architecture questions
Measure: time to answer using graph
Result: <2 seconds per query (just reading JSON)
```

## Iteration Goals

**Iteration 1:** Hierarchical structure + basic integration (imports, calls)
- Success: Tree structure correct, all imports/calls mapped
- Time: 2-3 hours to implement

**Iteration 2:** Rich context + reverse lookups
- Success: Edges have parameters, usage counts, read/write distinction
- Time: 1-2 hours to enhance

**Iteration 3:** Flow analysis + crossroads
- Success: Data flows mapped, major junctions identified
- Time: 2-3 hours to analyze

**Total:** Working integration map in ~6-8 hours of focused work
