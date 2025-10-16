# FOLLOW-UP PROMPTS (Chain-of-Prompts Pattern)

## Follow-Up Prompt #1: Post-Implementation Validation

```
Review the generated integration map JSON against these validation tests:

1. HIERARCHY TEST: Navigate to myapp.models.user.User.save in the tree
   - Can you reach it by following children at each level?
   - Does it show integration_points with calls and called_by?
   
2. REVERSE LOOKUP TEST: Pick 3 frequently-called functions
   - Verify their "called_by" lists are complete
   - Check if any callers are missing
   
3. CROSSROAD TEST: Identify major module boundaries (api↔models)
   - Are they in global_integration_map.crossroads?
   - Do crossroads show integration patterns?
   
4. DATA FLOW TEST: Trace one complete flow (e.g., user login)
   - Is the path end-to-end complete?
   - Are all integration points shown?

Show me specific issues found in each test. Fix the top 3 highest-impact gaps first.
```

## Follow-Up Prompt #2: Integration Depth Enhancement

```
Examine integration points for richness. For 5 random function calls, verify:

1. PARAMETERS: Does the call edge show what arguments were passed?
2. DATA FLOW: Can you see where the data comes from and goes to?
3. CONTEXT: Is it clear WHY this integration exists? (API calling model, validation, etc.)
4. SIDE EFFECTS: Are mutations/writes noted? (database, cache, state)

Pick one integration type (e.g., "api_to_model calls") and make those edges RICH with full context. Show before/after for one example edge.
```

## Follow-Up Prompt #3: Crossroad Deep Dive

```
Focus on the most complex integration junction in the codebase. For this crossroad:

1. List all components that meet here
2. Show all integration patterns at this junction
3. Map data flows passing through
4. Identify side effects
5. Mark as critical_path if it's high-traffic

Create a detailed crossroad analysis for this junction. This becomes the template for analyzing other crossroads.
```

## Follow-Up Prompt #4: Alias Resolution Audit

```
Search the integration map for any unresolved aliases or FQN issues:

1. Check imports: any showing "json" or stdlib names incorrectly?
2. Check calls: any pointing to unresolved "<unknown>" that SHOULD be resolved?
3. Check relative imports: are they converted to absolute FQNs?
4. Check aliased imports: does "import X as Y" resolve correctly when Y is used?

Fix alias resolution for the module with most import issues first. Show the fix.
```

## Follow-Up Prompt #5: LLM Usability Test

```
Pretend you're Claude Code. Using ONLY the integration map (no file parsing), answer:

1. "Show me everything that calls User.save"
2. "What's the data flow for user authentication?"
3. "Which modules does the api package integrate with?"
4. "What writes to the User.email attribute?"
5. "Show me the inheritance hierarchy of UserManager"

For each question: 
- Can you answer it? Yes/No
- If no, what's missing from the map?
- How long did it take? (should be <5 seconds per question)

Fix the blocker preventing any "No" answers.
```

## Follow-Up Prompt #6: Performance Optimization

```
Run the analyzer on a medium codebase (100-200 files). Measure:

1. Total analysis time
2. Memory usage peak
3. Output JSON file size
4. Time to load JSON in Claude Code

If analysis >30 seconds or JSON >5MB:
- Identify bottleneck (parsing? tree building? edge extraction?)
- Find one optimization that gives 2x speedup
- Implement it without sacrificing integration richness
```

## Follow-Up Prompt #7: Edge Case Stress Test

```
Create a test Python file with edge cases:

```python
# test_edge_cases.py
import json as j
from .relative import something
from parent import *

@decorator_chain
@another_decorator
class TestClass(BaseA, BaseB):
    def method(self):
        x = self.attr
        self.attr = 42
        result = obj.a.b.c()
        dynamic = importlib.import_module(name)
```

Run analyzer on this file. Verify:
1. Alias "j" resolves to "json"
2. Relative import ".relative" resolves to absolute path
3. Star import tracked as "<star:parent>"
4. Both decorators captured in chain order
5. Multiple inheritance (BaseA, BaseB) tracked
6. Attribute read and write distinguished
7. Chained call obj.a.b.c() broken into edges
8. Dynamic import marked as "<dynamic_import>"

Fix any edge case handling that fails.
```

## Follow-Up Prompt #8: Integration Completeness Audit

```
For your actual codebase, check integration completeness:

1. Count total functions in codebase
2. Count total functions in integration map
3. Identify any missing functions → add them

4. Count total imports in codebase (grep "^import\|^from")
5. Count total import edges in map
6. Identify any missing imports → add them

7. Pick 10 random function calls in code
8. Verify all 10 are in the integration map
9. Fix any missing call edges

Goal: 100% coverage of components, >95% coverage of integration points.
```

## Chain-of-Prompts Usage Pattern

**Start:** Use refined prompt to generate initial integration map

**Iterate:** Use follow-up prompts in sequence to enhance:
1. Validate structure (Follow-Up #1)
2. Enrich integration context (Follow-Up #2)
3. Analyze crossroads (Follow-Up #3)
4. Fix aliases (Follow-Up #4)
5. Test LLM usability (Follow-Up #5)
6. Optimize performance (Follow-Up #6)
7. Handle edge cases (Follow-Up #7)
8. Audit completeness (Follow-Up #8)

**Result:** Comprehensive, battle-tested integration map

## Quick Reference: When to Use Which Follow-Up

| Issue | Follow-Up Prompt |
|-------|------------------|
| Missing functions/classes | #8 Completeness Audit |
| Shallow edges (no context) | #2 Integration Depth |
| Can't answer LLM queries | #5 LLM Usability Test |
| Broken aliases | #4 Alias Resolution |
| Missing crossroads | #3 Crossroad Deep Dive |
| Slow analysis | #6 Performance |
| Edge case failures | #7 Stress Test |
| Structural issues | #1 Validation |
