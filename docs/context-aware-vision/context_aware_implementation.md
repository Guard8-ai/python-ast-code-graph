# Context-Aware Implementation Instructions

## Compression Architecture

### Layer 1: ID-Based References (Primary Optimization)

**Goal:** Replace repeated FQN strings with integer IDs

**Implementation:**
```python
class ComponentIndexer:
    def __init__(self):
        self.fqn_to_id = {}  # "myapp.models.User" → 142
        self.id_to_fqn = {}  # 142 → "myapp.models.User"
        self.next_id = 1
    
    def get_or_create_id(self, fqn: str) -> int:
        if fqn not in self.fqn_to_id:
            self.fqn_to_id[fqn] = self.next_id
            self.id_to_fqn[self.next_id] = fqn
            self.next_id += 1
        return self.fqn_to_id[fqn]
    
    def to_json_index(self) -> dict:
        # Compact index for JSON output
        return {str(id): fqn for id, fqn in self.id_to_fqn.items()}
```

**Usage:**
```python
indexer = ComponentIndexer()

# During AST traversal
user_class_id = indexer.get_or_create_id("myapp.models.user.User")
save_method_id = indexer.get_or_create_id("myapp.models.user.User.save")

# Store edge with IDs instead of strings
edge = {
    "s": save_method_id,  # source
    "t": logger_id,       # target
    "ty": "c",           # type: call
    "l": 45              # line
}
```

**Token Savings:**
- Before: `"myapp.models.user.User.save"` × 100 occurrences = 3,200 tokens
- After: `142` × 100 occurrences + 1 index entry = 300 tokens
- **Savings: 90%**

### Layer 2: Abbreviated Keys

**Key Mapping:**
```python
KEY_ABBREV = {
    # Core structure
    "type": "t",
    "name": "n",
    "parent": "p",
    "children": "ch",
    "line_range": "lr",
    "line": "l",
    "docstring": "doc",
    
    # Integration
    "source": "s",
    "target": "t",
    "args": "a",
    "returns": "ret",
    "calls": "c",
    "called_by": "cb",
    "reads": "rd",
    "writes": "wr",
    
    # Metadata
    "file": "f",
    "path": "pth",
    "integration_points": "ip",
    "usage_count": "uc",
    "confidence": "conf"
}

# Type codes
TYPE_CODES = {
    "package": "pk",
    "module": "mo",
    "class": "c",
    "function": "f",
    "method": "m",
    "attribute": "a"
}

# Integration type codes
INTEGRATION_CODES = {
    "import": "im",
    "call": "c",
    "inherit": "in",
    "attribute_read": "ar",
    "attribute_write": "aw",
    "decorator": "d"
}
```

**Apply Abbreviations:**
```python
def abbreviate_keys(data: dict) -> dict:
    """Recursively abbreviate dictionary keys"""
    if isinstance(data, dict):
        return {
            KEY_ABBREV.get(k, k): abbreviate_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [abbreviate_keys(item) for item in data]
    return data
```

### Layer 3: Flat Component Structure

**Before (Nested):**
```json
{
  "myapp": {
    "children": {
      "models": {
        "children": {
          "user": {
            "children": {
              "User": {
                "methods": {
                  "save": {...}
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

**After (Flat):**
```json
{
  "c": [
    {"id": 1, "t": "pk", "n": "myapp", "p": null},
    {"id": 2, "t": "mo", "n": "models", "p": 1},
    {"id": 3, "t": "mo", "n": "user", "p": 2},
    {"id": 4, "t": "c", "n": "User", "p": 3},
    {"id": 5, "t": "m", "n": "save", "p": 4, "lr": [42,56]}
  ]
}
```

**Implementation:**
```python
def flatten_hierarchy(tree: dict, indexer: ComponentIndexer) -> list:
    """Convert nested tree to flat component list"""
    components = []
    
    def traverse(node, parent_id=None):
        # Get or create ID for this component
        fqn = node["fqn"]
        comp_id = indexer.get_or_create_id(fqn)
        
        # Create flat component
        component = {
            "id": comp_id,
            "t": TYPE_CODES[node["type"]],
            "n": node["name"],
            "p": parent_id
        }
        
        # Add optional fields only if present
        if "line_range" in node:
            component["lr"] = node["line_range"]
        if "docstring" in node:
            component["doc"] = node["docstring"][:50]  # Truncate docs
        
        components.append(component)
        
        # Traverse children
        for child in node.get("children", {}).values():
            traverse(child, comp_id)
    
    traverse(tree)
    return components
```

### Layer 4: Array-Based Edges

**Compact Edge Format:**
```python
# Edge tuple: [source_id, target_id, type_code, line, optional_data]
# Types: c=call, im=import, ar=attr_read, aw=attr_write, in=inherit

def encode_edge(edge: dict, indexer: ComponentIndexer) -> list:
    """Convert edge dict to compact array"""
    source_id = indexer.get_or_create_id(edge["source"])
    target_id = indexer.get_or_create_id(edge["target"])
    
    # Base tuple
    encoded = [
        source_id,
        target_id,
        INTEGRATION_CODES[edge["type"]],
        edge.get("line", 0)
    ]
    
    # Optional data (only if present)
    optional = {}
    if "args" in edge:
        optional["a"] = edge["args"]
    if "returns" in edge:
        optional["ret"] = True
    
    if optional:
        encoded.append(optional)
    
    return encoded

# Example output
edges = [
    [142, 89, "c", 45, {"a": ["force"], "ret": true}],  # call with args
    [142, 91, "c", 54],                                  # simple call
    [143, 142, "cb", 78]                                 # reverse lookup
]
```

### Layer 5: Minified JSON Output

**Implementation:**
```python
import json

def write_compact_json(data: dict, filepath: str):
    """Write JSON without whitespace"""
    with open(filepath, 'w') as f:
        json.dump(
            data,
            f,
            separators=(',', ':'),  # No spaces
            ensure_ascii=False,
            sort_keys=False
        )

def write_readable_json(data: dict, filepath: str):
    """Write human-readable JSON"""
    with open(filepath, 'w') as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )
```

### Layer 6: Deduplication

**Remove Redundant Data:**
```python
def deduplicate_metadata(components: list) -> tuple[list, dict]:
    """Extract common metadata to separate section"""
    
    # Find common attributes across components
    file_map = {}  # file_id → filepath
    
    for comp in components:
        if "file" in comp:
            file_path = comp["file"]
            if file_path not in file_map:
                file_map[file_path] = len(file_map) + 1
            # Replace filepath with file_id
            comp["fid"] = file_map[file_path]
            del comp["file"]
    
    # Reverse mapping for output
    files = {fid: path for path, fid in file_map.items()}
    
    return components, files
```

## Complete Pipeline

```python
class ContextAwareMapper:
    def __init__(self, context_aware: bool = False):
        self.context_aware = context_aware
        self.indexer = ComponentIndexer()
    
    def generate_map(self, tree: dict, edges: list) -> dict:
        if not self.context_aware:
            # Return verbose format
            return self._verbose_output(tree, edges)
        
        # Context-aware pipeline
        
        # 1. Flatten hierarchy
        flat_components = flatten_hierarchy(tree, self.indexer)
        
        # 2. Deduplicate metadata
        flat_components, file_map = deduplicate_metadata(flat_components)
        
        # 3. Abbreviate keys
        flat_components = abbreviate_keys(flat_components)
        
        # 4. Encode edges as arrays
        encoded_edges = [
            encode_edge(edge, self.indexer)
            for edge in edges
        ]
        
        # 5. Build crossroads (keep compact)
        crossroads = self._build_crossroads_compact(edges)
        
        # 6. Assemble output
        output = {
            "v": "2.0-compact",
            "meta": {
                "ts": datetime.now().isoformat(),
                "stats": {
                    "c": len(flat_components),
                    "e": len(encoded_edges)
                }
            },
            "idx": self.indexer.to_json_index(),
            "files": file_map,
            "c": flat_components,
            "e": encoded_edges,
            "x": crossroads
        }
        
        return output
    
    def write(self, data: dict, filepath: str, readable: bool = False):
        if readable:
            write_readable_json(data, filepath)
        else:
            write_compact_json(data, filepath)
```

## CLI Integration

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--output', default='integration_map.json')
    parser.add_argument('--context-aware', action='store_true',
                       help='Generate token-efficient compact format')
    parser.add_argument('--readable', action='store_true',
                       help='Pretty-print JSON (increases tokens)')
    parser.add_argument('--decode', 
                       help='Decode compact map to verbose format')
    
    args = parser.parse_args()
    
    if args.decode:
        decode_compact_map(args.decode, args.output)
        return
    
    # Generate map
    mapper = ContextAwareMapper(context_aware=args.context_aware)
    tree, edges = analyze_codebase(args.root)
    output = mapper.generate_map(tree, edges)
    
    mapper.write(output, args.output, readable=args.readable)
    
    # Report token count
    estimate_tokens(args.output)
```

## Token Estimation

```python
def estimate_tokens(filepath: str) -> int:
    """Estimate token count (rough approximation)"""
    with open(filepath) as f:
        content = f.read()
    
    # Rough estimate: ~4 chars per token for JSON
    token_count = len(content) // 4
    
    print(f"Estimated tokens: {token_count:,}")
    return token_count
```

## Decoder Utility

```python
def decode_compact_map(compact_path: str, output_path: str):
    """Expand compact map to verbose format"""
    with open(compact_path) as f:
        compact = json.load(f)
    
    if compact.get("v") != "2.0-compact":
        print("Not a compact format file")
        return
    
    # Reverse abbreviations
    verbose = expand_keys(compact)
    
    # Expand IDs to FQNs
    idx = verbose["idx"]
    verbose = replace_ids_with_fqns(verbose, idx)
    
    # Expand edge arrays to dicts
    verbose["edges"] = [
        expand_edge_array(edge, idx)
        for edge in verbose["e"]
    ]
    del verbose["e"]
    
    # Write verbose output
    write_readable_json(verbose, output_path)
    print(f"Decoded to {output_path}")
```

## Expected Results

**Before Context-Aware Mode:**
```
File: 556 KB / 25,830 lines / 190,068 tokens
Problem: Consumes 95% of Claude Code's context
```

**After Context-Aware Mode:**
```
File: 95 KB / 3,200 lines / 25,000 tokens
Result: Consumes 12.5% of Claude Code's context
Savings: 85% token reduction
```

## Testing Strategy

```python
# Test token reduction
def test_compression():
    # Generate both formats
    verbose_map = generate_map(context_aware=False)
    compact_map = generate_map(context_aware=True)
    
    # Compare token counts
    verbose_tokens = estimate_tokens(verbose_map)
    compact_tokens = estimate_tokens(compact_map)
    
    reduction = (verbose_tokens - compact_tokens) / verbose_tokens
    assert reduction >= 0.80, f"Expected 80%+ reduction, got {reduction:.1%}"
    
    # Verify information preservation
    verbose_data = load_map(verbose_map)
    compact_data = decode_compact_map(compact_map)
    
    assert_equal_info(verbose_data, compact_data)
```

## Migration Path

1. **Keep backward compatibility:** Default mode unchanged
2. **Add flag:** `--context-aware` enables new mode
3. **Test both modes:** Verify same information
4. **Document difference:** README explains token savings
5. **Provide decoder:** Users can expand compact → verbose
