# Context-Aware Vision: Token-Efficient Architecture Map

## The Problem

**Current State:**
- Generated file: 556.84 KB / 25,830 lines / 190,068 tokens
- Claude Code's context window: ~200,000 tokens
- Result: File consumes 95% of available context
- **Critical failure:** Claude Code can't analyze the map AND work with code simultaneously

**Root Causes:**
1. **Verbose keys:** `"integration_points"`, `"data_flows"`, `"fully_qualified_name"` (high repetition)
2. **Repeated FQNs:** `"myapp.models.user.User.save"` appears hundreds of times
3. **Deep nesting:** 6-8 levels of JSON depth with full context at each level
4. **Redundant metadata:** Same information duplicated across nodes
5. **Pretty-printed JSON:** Whitespace and formatting adds 30-40% overhead

## The Vision: Token-Efficient Integration Map

**Target:**
- Same codebase analysis: <30,000 tokens (85% reduction)
- Claude Code uses 15% context for map, 85% for actual work
- Zero information loss (compress, don't truncate)
- Backward compatible with `--context-aware` flag

**Core Philosophy:**
> "Every byte counts. Maximum information density. Zero redundancy."

## Compression Strategies

### 1. ID-Based References (70% reduction)
**Before:**
```json
{
  "source": "myapp.models.user.User.save",
  "target": "myapp.utils.logger.log_action",
  "called_by": [
    "myapp.api.endpoints.create_user",
    "myapp.api.endpoints.update_user"
  ]
}
```

**After:**
```json
{
  "s": 142,
  "t": 89,
  "cb": [203, 204]
}
```
With separate index:
```json
{
  "idx": {
    "142": "myapp.models.user.User.save",
    "89": "myapp.utils.logger.log_action",
    "203": "myapp.api.endpoints.create_user"
  }
}
```

### 2. Abbreviated Keys (40% reduction)
```json
// Verbose (82 chars)
{"integration_points": {...}, "fully_qualified_name": "...", "line_range": [1,10]}

// Compact (34 chars)
{"ip": {...}, "fqn": "...", "lr": [1,10]}
```

### 3. Flat Reference Structure (60% reduction)
**Before:** Nested hierarchy with full context at each level  
**After:** Flat component list + separate relationship map

```json
{
  "c": {  // components
    "142": {"t": "m", "n": "save", "p": 141, "l": [42, 56]},
    "141": {"t": "c", "n": "User", "p": 140}
  },
  "r": [  // relationships
    {"s": 142, "t": 89, "ty": "call", "l": 45}
  ]
}
```

### 4. Array-Based Edges (50% reduction)
**Before:**
```json
{
  "source": "func_a",
  "target": "func_b", 
  "type": "call",
  "line": 42,
  "args": ["param1", "param2"]
}
```

**After:**
```json
[142, 89, "c", 42, ["param1", "param2"]]
// [source_id, target_id, type_code, line, args]
```

### 5. Type Codes (30% reduction)
```json
// Instead of "type": "function"
"t": "f"  // f=function, c=class, m=method, p=package, mo=module
```

### 6. Minified Output (30% reduction)
- No pretty-printing by default
- Optional `--readable` flag for human inspection
- Claude Code doesn't need whitespace

## Target Schema (Context-Aware Mode)

```json
{
  "v": "2.0-compact",
  "meta": {
    "ts": "2025-10-16T10:30:00Z",
    "root": "/project",
    "stats": {"c": 1847, "r": 5392}
  },
  
  "idx": {
    "1": "myapp",
    "2": "myapp.models",
    "3": "myapp.models.user",
    "4": "myapp.models.user.User",
    "5": "myapp.models.user.User.save"
  },
  
  "c": [
    {"id": 5, "t": "m", "p": 4, "lr": [42,56], "doc": "Save user..."},
    {"id": 4, "t": "c", "p": 3, "lr": [15,89], "b": [99]}
  ],
  
  "e": [
    [5, 89, "c", 45, {"args": ["force"], "ret": true}],
    [5, 91, "c", 54, {"args": ["self.username"]}]
  ],
  
  "x": [
    {"id": "api_models", "c": [1, 2], "cnt": 45}
  ]
}
```

**Key Mappings:**
- `v`: version
- `meta`: metadata
- `ts`: timestamp
- `c`: count
- `r`: relationships
- `idx`: index (ID → FQN)
- `c`: components (was codebase_tree)
- `id`: component ID
- `t`: type
- `p`: parent ID
- `lr`: line range
- `doc`: docstring
- `b`: bases (inheritance)
- `e`: edges (was integration_points)
- `x`: crossroads
- `cnt`: count

## Token Budget Breakdown

**Target: 30,000 tokens for 500-file codebase**

```
Index (ID→FQN mapping):        3,000 tokens  (10%)
Components (flat list):        12,000 tokens (40%)
Edges (relationships):         10,000 tokens (33%)
Crossroads (junctions):        3,000 tokens  (10%)
Metadata:                      2,000 tokens  (7%)
---
Total:                         30,000 tokens (100%)
```

## Implementation Strategy

**Phase 1: Dual-Mode Output**
- Keep existing verbose mode (default)
- Add `--context-aware` flag for compact mode
- Both modes have same information, different encoding

**Phase 2: Optimize Existing**
- Replace verbose keys with abbreviations
- Implement ID-based references
- Use type codes instead of strings

**Phase 3: Advanced Compression**
- Array-based edge format
- Minified JSON output
- Integer-encoded types

## Success Metrics

✅ **Token Reduction:**
- From 190,000 tokens → <30,000 tokens (85% reduction)
- Claude Code uses <15% context for map

✅ **Information Preservation:**
- Zero data loss (all relationships preserved)
- Same query capabilities
- Lossless compression only

✅ **Usability:**
- Flag-based: `--context-aware` enables compact mode
- Default mode unchanged (backward compatible)
- Decoder utility to expand compact → verbose

## Usage Pattern

```bash
# Verbose mode (current)
python integration_mapper.py --root ./project --output map.json

# Context-aware mode (new)
python integration_mapper.py --root ./project --output map.json --context-aware

# Decode compact map for human reading
python integration_mapper.py --decode map.json --readable
```

## Why This Matters

**Before (Verbose Mode):**
- Load map: 190K tokens
- Remaining context: 10K tokens
- Claude Code: "I don't have room to work"

**After (Context-Aware Mode):**
- Load map: 25K tokens
- Remaining context: 175K tokens
- Claude Code: "I can analyze architecture AND implement changes"

## Key Principle

> "Compress intelligently. Reference, don't repeat. Count every token."

The map should be a dense index, not a verbose document.
