# Context-Aware Integration Mapper: Implementation Prompt

## Mission

Implement context-aware mode for the integration mapper that reduces output from 190K tokens to <30K tokens (85% reduction) through intelligent compression while preserving all information.

## The Problem

**Current State:**
- Generated integration map: 556 KB / 25,830 lines / 190,068 tokens
- Claude Code context window: ~200,000 tokens  
- **Critical issue:** Map consumes 95% of context, leaving no room for actual code work

**Required Solution:**
- New `--context-aware` flag that generates compressed format
- Target: <30,000 tokens (85% reduction)
- Zero information loss (compress, don't truncate)
- Backward compatible (default mode unchanged)

## Implementation Strategy

You'll implement this in 9 tasks using **taskguard** for task management:

### Task Flow
```
1. Create ComponentIndexer (FQN → integer ID mapping)
2. Create abbreviation mappings (long keys → short keys)
3. Create BaseFormatter abstraction (pluggable formats)
4. Refactor existing to VerboseFormatter (default mode)
5. Implement CompactFormatter (context-aware mode)
6. Create decoder utility (compact → verbose expansion)
7. Add CLI flags (--context-aware, --decode)
8. Add comprehensive tests (verify 80%+ reduction)
9. Update documentation (README with new features)
```

## Core Compression Techniques

### 1. ID-Based References (60% reduction)
```python
# Before: Repeated FQNs
{"source": "myapp.models.user.User.save", "target": "myapp.utils.logger.log"}

# After: Integer IDs + index
{"s": 142, "t": 89}  # Plus: {"idx": {"142": "myapp.models.user.User.save", ...}}
```

### 2. Abbreviated Keys (20% reduction)
```python
# Before: Long keys
{"type": "method", "name": "save", "line_range": [42, 56]}

# After: Short keys  
{"t": "m", "n": "save", "lr": [42, 56]}
```

### 3. Flat Structure (15% reduction)
```python
# Before: Deep nesting (6-8 levels)
{"myapp": {"children": {"models": {"children": {...}}}}}

# After: Flat list with parent IDs
[{"id": 1, "n": "myapp", "p": null}, {"id": 2, "n": "models", "p": 1}]
```

### 4. Array Edges (10% reduction)
```python
# Before: Verbose dicts
{"source": "func_a", "target": "func_b", "type": "call", "line": 42}

# After: Compact arrays
[142, 89, "c", 42]  # [source_id, target_id, type_code, line]
```

### 5. Minified Output (10% reduction)
```python
# No pretty-printing, no whitespace
json.dump(data, f, separators=(',', ':'))
```

## Taskguard Workflow (CRITICAL)

For EVERY task, follow this exact workflow:

### Step 1: Create Task
```bash
taskguard create "<task description>" \
  --branch context-optimization/<task-name> \
  --parent context-optimization \
  --type <feature|refactor|test|docs>
```

### Step 2: Switch to Task Branch
```bash
# Taskguard should automatically switch, or manually:
git checkout context-optimization/<task-name>
```

### Step 3: Implement Changes
- Write code following the task requirements
- Add proper docstrings and type hints
- Keep changes focused on single task

### Step 4: Commit as User (NOT as AI agent)
```bash
git add <files>
git commit -m "feat|refactor|test|docs: <short description>

<detailed multi-line description of changes>
<explain the why, not just the what>"

# Example:
git commit -m "feat: implement ComponentIndexer for FQN-to-ID mapping

- Add ComponentIndexer class with bidirectional mapping
- Support get_or_create_id() for ID assignment  
- Add to_json_index() for JSON export
- Foundation for 60% token reduction through ID references"
```

### Step 5: Update Task Status
```bash
taskguard update --status in-progress
```

### Step 6: Test and Validate
```bash
# Run tests specific to this task
pytest tests/test_<component>.py

# Validate with taskguard
taskguard validate
```

### Step 7: Complete Task
```bash
taskguard update --status completed
```

### Step 8: Merge to Parent (when ready)
```bash
git checkout context-optimization
git merge context-optimization/<task-name>
```

## Epic Setup

Before starting tasks, set up the epic branch:

```bash
# Create epic branch from main
git checkout main
git checkout -b context-optimization

# Create epic task (if supported)
taskguard create "Context-Aware Integration Map (85% Token Reduction)" \
  --type epic \
  --description "Reduce integration map from 190K to <30K tokens while preserving all information"

# Commit initial setup
git commit --allow-empty -m "feat: initialize context-optimization epic

Epic Goal: Reduce integration map token usage by 85%
- Implement ID-based references  
- Add key abbreviations
- Flatten hierarchy structure
- Use array-based edges
- Output minified JSON
- Maintain backward compatibility"
```

## Task-by-Task Implementation

### Task 1: ComponentIndexer (30 min)

**Create:** `utils/indexer.py`

**Code:**
```python
class ComponentIndexer:
    """Maps fully qualified names to integer IDs for compression"""
    
    def __init__(self):
        self.fqn_to_id: dict[str, int] = {}
        self.id_to_fqn: dict[int, str] = {}
        self.next_id = 1
    
    def get_or_create_id(self, fqn: str) -> int:
        """Get existing ID or assign new one"""
        if fqn not in self.fqn_to_id:
            self.fqn_to_id[fqn] = self.next_id
            self.id_to_fqn[self.next_id] = fqn
            self.next_id += 1
        return self.fqn_to_id[fqn]
    
    def to_json_index(self) -> dict[str, str]:
        """Export index for JSON output"""
        return {str(id): fqn for id, fqn in self.id_to_fqn.items()}
```

**Taskguard:**
```bash
taskguard create "Implement ComponentIndexer for FQN-to-ID mapping" \
  --branch context-optimization/indexer --parent context-optimization --type feature

# Code...

git add utils/indexer.py utils/__init__.py
git commit -m "feat: implement ComponentIndexer for FQN-to-ID mapping"
taskguard validate && taskguard update --status completed
```

### Task 2: Abbreviation Mappings (30 min)

**Create:** `utils/abbreviations.py`

**Code:**
```python
KEY_ABBREV = {
    "type": "t", "name": "n", "parent": "p", "children": "ch",
    "line_range": "lr", "line": "l", "docstring": "doc",
    "source": "s", "target": "t", "args": "a", "returns": "ret",
    # ... more mappings
}

TYPE_CODES = {
    "package": "pk", "module": "mo", "class": "c",
    "function": "f", "method": "m", "attribute": "a"
}

INTEGRATION_CODES = {
    "import": "im", "call": "c", "inherit": "in",
    "attribute_read": "ar", "attribute_write": "aw", "decorator": "d"
}

def abbreviate_keys(data):
    """Recursively abbreviate dictionary keys"""
    if isinstance(data, dict):
        return {KEY_ABBREV.get(k, k): abbreviate_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [abbreviate_keys(item) for item in data]
    return data

def expand_keys(data):
    """Reverse abbreviation for decoding"""
    REVERSE = {v: k for k, v in KEY_ABBREV.items()}
    if isinstance(data, dict):
        return {REVERSE.get(k, k): expand_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [expand_keys(item) for item in data]
    return data
```

### Task 5: CompactFormatter (2 hours) - CRITICAL

**Create:** `formatters/compact_formatter.py`

**Key Methods:**
```python
class CompactFormatter(BaseFormatter):
    def __init__(self):
        self.indexer = ComponentIndexer()
    
    def format_components(self, tree: dict) -> list:
        """Flatten hierarchy to component list with parent IDs"""
        components = []
        def traverse(node, parent_id=None):
            comp_id = self.indexer.get_or_create_id(node["fqn"])
            component = {
                "id": comp_id,
                "t": TYPE_CODES[node["type"]],
                "n": node["name"],
                "p": parent_id
            }
            if "line_range" in node:
                component["lr"] = node["line_range"]
            components.append(component)
            
            for child in node.get("children", {}).values():
                traverse(child, comp_id)
        traverse(tree)
        return components
    
    def format_edges(self, edges: list) -> list:
        """Convert edges to compact array format"""
        compact = []
        for edge in edges:
            src_id = self.indexer.get_or_create_id(edge["source"])
            tgt_id = self.indexer.get_or_create_id(edge["target"])
            compact_edge = [src_id, tgt_id, INTEGRATION_CODES[edge["type"]], edge.get("line", 0)]
            
            optional = {}
            if "args" in edge: optional["a"] = edge["args"]
            if "returns" in edge: optional["ret"] = True
            if optional: compact_edge.append(optional)
            
            compact.append(compact_edge)
        return compact
    
    def build_output(self, components, edges, metadata) -> dict:
        return {
            "v": "2.0-compact",
            "meta": abbreviate_keys(metadata),
            "idx": self.indexer.to_json_index(),
            "c": components,
            "e": edges
        }
    
    def write(self, data: dict, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(data, f, separators=(',', ':'))  # Minified
```

### Task 7: CLI Integration (1 hour)

**Modify:** `integration_mapper.py`

**Key Changes:**
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--output', default='integration_map.json')
    parser.add_argument('--context-aware', action='store_true',
                       help='Generate token-efficient format (85%% reduction)')
    parser.add_argument('--decode', help='Decode compact map to verbose format')
    
    args = parser.parse_args()
    
    # Decode mode
    if args.decode:
        from utils.decoder import CompactDecoder
        CompactDecoder.decode_file(args.decode, args.output)
        return
    
    # Analysis mode
    analyzer = CodebaseAnalyzer(args.root)
    tree, edges = analyzer.analyze()
    
    # Choose formatter
    if args.context_aware:
        from formatters.compact_formatter import CompactFormatter
        formatter = CompactFormatter()
    else:
        from formatters.verbose_formatter import VerboseFormatter
        formatter = VerboseFormatter()
    
    # Generate output
    output = formatter.build_output(...)
    formatter.write(output, args.output)
    
    # Report token count
    token_count = estimate_tokens(args.output)
    print(f"Estimated tokens: {token_count:,}")
```

## Validation Criteria

After implementing all tasks, verify:

### Token Reduction Test
```bash
# Generate both formats
python integration_mapper.py --root ./test_project --output verbose.json
python integration_mapper.py --root ./test_project --output compact.json --context-aware

# Compare tokens
python -c "
import json
v = len(json.dumps(json.load(open('verbose.json')))) // 4
c = len(json.dumps(json.load(open('compact.json')))) // 4
print(f'Verbose: {v:,} tokens')
print(f'Compact: {c:,} tokens')
print(f'Reduction: {(v-c)/v:.1%}')
"

# Expected: ≥80% reduction
```

### Information Preservation Test
```bash
# Round-trip test
python integration_mapper.py --decode compact.json --output decoded.json

# Verify equivalence (structurally, not byte-for-byte)
python -c "
import json
v = json.load(open('verbose.json'))
d = json.load(open('decoded.json'))
# Compare component counts, edge counts, etc.
"
```

### Integration Test
```bash
# Test both modes work end-to-end
pytest tests/test_compression.py -v
```

## Success Criteria

✅ **Token Reduction:** Verbose 190K → Compact <30K (≥80% reduction)  
✅ **Backward Compatibility:** Default mode unchanged, all existing tests pass  
✅ **Information Preservation:** Round-trip lossless (compact → decode → verbose equivalent)  
✅ **CLI Usability:** `--context-aware` and `--decode` flags work correctly  
✅ **Code Quality:** Type hints, docstrings, tests, documentation  

## Timeline

- Task 1-2: Foundations (1 hour)
- Task 3-4: Refactoring (1.5 hours)
- Task 5-6: Core implementation (3 hours)
- Task 7-9: Integration & docs (3 hours)

**Total:** 8-9 hours of focused work

## Key Principles

1. **Use taskguard for EVERY task** - create, update, validate, complete
2. **Commit as user** - not as AI agent
3. **One task at a time** - don't jump ahead
4. **Test before completing** - taskguard validate
5. **Parent branch:** All tasks under `context-optimization` epic

## Getting Started

```bash
# Step 1: Create epic branch
git checkout -b context-optimization

# Step 2: Start with Task 1
taskguard create "Implement ComponentIndexer for FQN-to-ID mapping" \
  --branch context-optimization/indexer \
  --parent context-optimization \
  --type feature

# Step 3: Follow the workflow for each task

# Step 4: After all tasks, merge to main
git checkout main
git merge context-optimization
git tag -a v2.0.0-context-aware -m "Add context-aware mode with 85% token reduction"
```

Now begin with Task 1. Create the task, implement ComponentIndexer, test, commit, and complete before moving to Task 2.
