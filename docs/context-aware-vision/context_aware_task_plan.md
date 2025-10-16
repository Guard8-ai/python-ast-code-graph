# Context-Aware Changes: Master Task Plan

## Epic Overview

**Epic Branch:** `context-optimization`  
**Goal:** Reduce integration map tokens from 190K → 25K (85% reduction)  
**Impact:** Enable Claude Code to use map AND work with code simultaneously  
**Backward Compatibility:** Default mode unchanged, opt-in via `--context-aware` flag

## Task Hierarchy

```
Epic: context-optimization
├── Task 1: Create component indexer (utils/indexer.py)
├── Task 2: Create abbreviation mappings (utils/abbreviations.py)
├── Task 3: Create base formatter abstraction (formatters/base_formatter.py)
├── Task 4: Refactor to use formatter pattern (formatters/verbose_formatter.py)
├── Task 5: Implement compact formatter (formatters/compact_formatter.py)
├── Task 6: Create decoder utility (utils/decoder.py)
├── Task 7: Add CLI flags and integration (integration_mapper.py)
├── Task 8: Add tests and validation (tests/test_compression.py)
└── Task 9: Update documentation (README.md)
```

---

## Task 1: Create Component Indexer

**Branch:** `context-optimization/indexer`  
**File:** `utils/indexer.py`  
**Estimated Time:** 30 minutes  
**Dependencies:** None

### Description
Create ComponentIndexer class that maps fully qualified names (FQNs) to integer IDs for compression.

### Acceptance Criteria
- [ ] ComponentIndexer class with `get_or_create_id(fqn)` method
- [ ] Bidirectional mapping (FQN↔ID)
- [ ] `to_json_index()` method for export
- [ ] Unit tests pass

### Taskguard Workflow
```bash
# Create task
taskguard create "Implement ComponentIndexer for FQN-to-ID mapping" \
  --branch context-optimization/indexer \
  --parent context-optimization \
  --type feature

# Work on task
# ... implement utils/indexer.py ...

# Commit as user
git add utils/indexer.py
git commit -m "feat: implement ComponentIndexer for FQN-to-ID mapping

- Add ComponentIndexer class with bidirectional mapping
- Support get_or_create_id() for ID assignment
- Add to_json_index() for JSON export
- Foundation for 60% token reduction through ID references"

# Update task
taskguard update --status in-progress

# After testing
taskguard validate
taskguard update --status completed
```

### Implementation Checklist
- [ ] Create `utils/` directory
- [ ] Create `utils/__init__.py`
- [ ] Create `utils/indexer.py` with ComponentIndexer class
- [ ] Add docstrings and type hints
- [ ] Test with sample FQNs

---

## Task 2: Create Abbreviation Mappings

**Branch:** `context-optimization/abbreviations`  
**File:** `utils/abbreviations.py`  
**Estimated Time:** 30 minutes  
**Dependencies:** None

### Description
Define mappings for key abbreviation (type→t, name→n) and helper functions for abbreviating/expanding keys.

### Acceptance Criteria
- [ ] KEY_ABBREV dict with all common keys
- [ ] TYPE_CODES dict for component types
- [ ] INTEGRATION_CODES dict for edge types
- [ ] `abbreviate_keys()` function (recursive)
- [ ] `expand_keys()` function for decoding

### Taskguard Workflow
```bash
taskguard create "Create abbreviation mappings and helper functions" \
  --branch context-optimization/abbreviations \
  --parent context-optimization \
  --type feature

# Implement...

git add utils/abbreviations.py
git commit -m "feat: add abbreviation mappings for key compression

- Define KEY_ABBREV for common JSON keys
- Add TYPE_CODES for component type compression  
- Add INTEGRATION_CODES for edge type compression
- Implement abbreviate_keys() recursive function
- Implement expand_keys() for decoding
- Enable 20% token reduction through key compression"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Create `utils/abbreviations.py`
- [ ] Define KEY_ABBREV mapping
- [ ] Define TYPE_CODES mapping
- [ ] Define INTEGRATION_CODES mapping
- [ ] Implement abbreviate_keys() function
- [ ] Implement expand_keys() function
- [ ] Add comprehensive docstrings

---

## Task 3: Create Base Formatter Abstraction

**Branch:** `context-optimization/base-formatter`  
**File:** `formatters/base_formatter.py`  
**Estimated Time:** 30 minutes  
**Dependencies:** None

### Description
Create abstract base class for output formatters to enable pluggable format implementations.

### Acceptance Criteria
- [ ] BaseFormatter abstract class
- [ ] Abstract methods: format_components, format_edges, build_output
- [ ] Docstrings explaining formatter contract

### Taskguard Workflow
```bash
taskguard create "Create BaseFormatter abstraction for pluggable formats" \
  --branch context-optimization/base-formatter \
  --parent context-optimization \
  --type feature

# Implement...

git add formatters/base_formatter.py formatters/__init__.py
git commit -m "feat: add BaseFormatter abstraction for pluggable formats

- Create abstract BaseFormatter class
- Define format_components() interface
- Define format_edges() interface
- Define build_output() interface
- Enable multiple format implementations (verbose/compact)"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Create `formatters/` directory
- [ ] Create `formatters/__init__.py`
- [ ] Create `formatters/base_formatter.py`
- [ ] Define BaseFormatter ABC
- [ ] Add abstract methods with docstrings

---

## Task 4: Refactor to Verbose Formatter

**Branch:** `context-optimization/verbose-formatter`  
**File:** `formatters/verbose_formatter.py`  
**Estimated Time:** 1 hour  
**Dependencies:** Task 3 (base-formatter)

### Description
Extract existing output logic into VerboseFormatter class to maintain backward compatibility.

### Acceptance Criteria
- [ ] VerboseFormatter extends BaseFormatter
- [ ] Implements all abstract methods
- [ ] Produces identical output to current implementation
- [ ] All existing tests pass

### Taskguard Workflow
```bash
taskguard create "Refactor existing output to VerboseFormatter" \
  --branch context-optimization/verbose-formatter \
  --parent context-optimization \
  --type refactor

# Implement...

git add formatters/verbose_formatter.py
git commit -m "refactor: extract existing output to VerboseFormatter

- Create VerboseFormatter implementing BaseFormatter
- Move hierarchical tree formatting logic
- Move edge formatting logic
- Maintain backward compatibility
- No behavior changes, just restructuring"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Create `formatters/verbose_formatter.py`
- [ ] Extend BaseFormatter
- [ ] Implement format_components() (nested tree)
- [ ] Implement format_edges() (full edge dicts)
- [ ] Implement build_output()
- [ ] Run existing tests to verify no regression

---

## Task 5: Implement Compact Formatter

**Branch:** `context-optimization/compact-formatter`  
**File:** `formatters/compact_formatter.py`  
**Estimated Time:** 2 hours  
**Dependencies:** Task 1 (indexer), Task 2 (abbreviations), Task 3 (base-formatter)

### Description
Implement CompactFormatter with ID-based references, abbreviated keys, flat structure, and array edges.

### Acceptance Criteria
- [ ] CompactFormatter extends BaseFormatter
- [ ] Uses ComponentIndexer for FQN→ID mapping
- [ ] Flattens hierarchy to component list
- [ ] Converts edges to compact array format
- [ ] Applies key abbreviations
- [ ] Outputs minified JSON
- [ ] Achieves 80%+ token reduction

### Taskguard Workflow
```bash
taskguard create "Implement CompactFormatter for token-efficient output" \
  --branch context-optimization/compact-formatter \
  --parent context-optimization \
  --type feature

# Implement...

git add formatters/compact_formatter.py
git commit -m "feat: implement CompactFormatter for 85% token reduction

- Create CompactFormatter with ComponentIndexer integration
- Flatten nested hierarchy to component list with parent IDs
- Convert edges to compact array format [src, tgt, type, line]
- Apply key abbreviations (type→t, name→n, etc.)
- Output minified JSON (no whitespace)
- Achieve target 80%+ token reduction vs verbose mode"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Create `formatters/compact_formatter.py`
- [ ] Initialize ComponentIndexer
- [ ] Implement flatten_hierarchy() helper
- [ ] Implement format_components() with ID refs
- [ ] Implement format_edges() as arrays
- [ ] Apply abbreviate_keys()
- [ ] Implement minified write()
- [ ] Test on sample codebase
- [ ] Verify token count reduction

---

## Task 6: Create Decoder Utility

**Branch:** `context-optimization/decoder`  
**File:** `utils/decoder.py`  
**Estimated Time:** 1 hour  
**Dependencies:** Task 2 (abbreviations), Task 5 (compact-formatter)

### Description
Create utility to decode compact format back to verbose format for human inspection.

### Acceptance Criteria
- [ ] CompactDecoder class
- [ ] decode_file() method
- [ ] Expands IDs to FQNs
- [ ] Expands abbreviated keys
- [ ] Converts edge arrays to dicts
- [ ] Outputs readable JSON

### Taskguard Workflow
```bash
taskguard create "Create CompactDecoder for format expansion" \
  --branch context-optimization/decoder \
  --parent context-optimization \
  --type feature

# Implement...

git add utils/decoder.py
git commit -m "feat: add CompactDecoder for expanding compact maps

- Create CompactDecoder with decode_file() method
- Expand integer IDs back to FQNs using index
- Reverse key abbreviations (t→type, n→name, etc.)
- Convert edge arrays back to dictionaries
- Output human-readable pretty-printed JSON
- Enable inspection of compact maps"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Create `utils/decoder.py`
- [ ] Implement CompactDecoder class
- [ ] Implement decode_file() method
- [ ] Implement _expand_ids() helper
- [ ] Implement _expand_edge() helper
- [ ] Use expand_keys() from abbreviations
- [ ] Test round-trip: compact → decode → verbose

---

## Task 7: Add CLI Flags and Integration

**Branch:** `context-optimization/cli-integration`  
**File:** `integration_mapper.py`  
**Estimated Time:** 1 hour  
**Dependencies:** Task 4 (verbose-formatter), Task 5 (compact-formatter), Task 6 (decoder)

### Description
Integrate formatters into main CLI with --context-aware and --decode flags.

### Acceptance Criteria
- [ ] `--context-aware` flag added
- [ ] `--decode` flag added
- [ ] Formatter selection based on flags
- [ ] Token count reporting
- [ ] Help text updated
- [ ] Both modes work end-to-end

### Taskguard Workflow
```bash
taskguard create "Integrate formatters with CLI flags" \
  --branch context-optimization/cli-integration \
  --parent context-optimization \
  --type feature

# Implement...

git add integration_mapper.py
git commit -m "feat: add --context-aware and --decode CLI flags

- Add --context-aware flag to enable compact format
- Add --decode flag to expand compact maps
- Implement formatter selection logic
- Add token count estimation and reporting
- Update CLI help text
- Maintain backward compatibility (default is verbose)
- Enable end-to-end token-efficient workflow"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Import formatters and decoder
- [ ] Add argparse flags
- [ ] Implement formatter selection
- [ ] Add decode mode handling
- [ ] Add token estimation
- [ ] Update help text
- [ ] Test both modes

---

## Task 8: Add Tests and Validation

**Branch:** `context-optimization/tests`  
**File:** `tests/test_compression.py`  
**Estimated Time:** 1.5 hours  
**Dependencies:** All previous tasks

### Description
Create comprehensive tests to verify token reduction and information preservation.

### Acceptance Criteria
- [ ] Test token reduction (80%+ verified)
- [ ] Test information preservation (compact ≈ verbose)
- [ ] Test round-trip (analyze → compact → decode → verbose)
- [ ] Test CLI flags
- [ ] All tests pass

### Taskguard Workflow
```bash
taskguard create "Add comprehensive compression tests" \
  --branch context-optimization/tests \
  --parent context-optimization \
  --type test

# Implement...

git add tests/test_compression.py tests/test_formatters.py
git commit -m "test: add comprehensive compression and formatter tests

- Test token reduction ≥80% vs verbose mode
- Test information preservation between formats
- Test round-trip: compact → decode → verbose equivalence
- Test CLI flags (--context-aware, --decode)
- Test ComponentIndexer, abbreviations, formatters
- Verify all acceptance criteria met"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Create `tests/` directory
- [ ] Create `tests/test_compression.py`
- [ ] Test token reduction
- [ ] Test information preservation
- [ ] Test round-trip
- [ ] Test CLI integration
- [ ] Run full test suite

---

## Task 9: Update Documentation

**Branch:** `context-optimization/docs`  
**File:** `README.md`  
**Estimated Time:** 45 minutes  
**Dependencies:** All previous tasks

### Description
Update README with context-aware mode documentation and usage examples.

### Acceptance Criteria
- [ ] Document --context-aware flag
- [ ] Document --decode flag
- [ ] Explain token savings
- [ ] Provide usage examples
- [ ] Update architecture section

### Taskguard Workflow
```bash
taskguard create "Update documentation for context-aware mode" \
  --branch context-optimization/docs \
  --parent context-optimization \
  --type docs

# Implement...

git add README.md
git commit -m "docs: add context-aware mode documentation

- Document --context-aware flag for token-efficient output
- Document --decode flag for format expansion
- Explain 85% token reduction benefits
- Add usage examples for both modes
- Update architecture diagram
- Clarify backward compatibility"

taskguard update --status completed
taskguard validate
```

### Implementation Checklist
- [ ] Add "Context-Aware Mode" section
- [ ] Document flags and options
- [ ] Add before/after token comparison
- [ ] Provide usage examples
- [ ] Update architecture diagram
- [ ] Proofread and verify

---

## Taskguard Workflow Summary

### Epic Setup
```bash
# Create epic branch
git checkout -b context-optimization

# Create epic tracker (if taskguard supports)
taskguard create "Context-Aware Integration Map" \
  --type epic \
  --description "Reduce integration map from 190K to 25K tokens"
```

### For Each Task
```bash
# 1. Create task and branch
taskguard create "<task description>" \
  --branch context-optimization/<task-name> \
  --parent context-optimization \
  --type <feature|refactor|test|docs>

# 2. Implement changes
# ... code ...

# 3. Commit as user (not as AI agent)
git add <files>
git commit -m "<conventional commit message>

<detailed description>"

# 4. Update task status
taskguard update --status in-progress

# 5. Test and validate
# ... run tests ...
taskguard validate

# 6. Complete task
taskguard update --status completed

# 7. Merge to parent (if ready)
git checkout context-optimization
git merge context-optimization/<task-name>
```

### Epic Completion
```bash
# After all tasks completed
git checkout main
git merge context-optimization

# Tag release
git tag -a v2.0.0-context-aware -m "Add context-aware mode with 85% token reduction"
```

---

## Timeline

| Task | Time | Cumulative |
|------|------|------------|
| Task 1: Indexer | 30m | 30m |
| Task 2: Abbreviations | 30m | 1h |
| Task 3: Base Formatter | 30m | 1.5h |
| Task 4: Verbose Formatter | 1h | 2.5h |
| Task 5: Compact Formatter | 2h | 4.5h |
| Task 6: Decoder | 1h | 5.5h |
| Task 7: CLI Integration | 1h | 6.5h |
| Task 8: Tests | 1.5h | 8h |
| Task 9: Documentation | 45m | 8h 45m |

**Total Estimated Time:** 8-9 hours

---

## Success Criteria (Epic-Level)

✅ **Token Reduction:**
- Verbose mode: ~190K tokens
- Context-aware mode: <30K tokens
- Reduction: ≥80%

✅ **Backward Compatibility:**
- Default behavior unchanged
- All existing tests pass
- No breaking changes

✅ **Information Preservation:**
- Compact format contains all data
- Round-trip lossless (compact → decode → verbose)
- Same query capabilities

✅ **Developer Experience:**
- Clear CLI flags
- Good documentation
- Easy to understand
- Opt-in (not forced)

✅ **Claude Code Usability:**
- Can load map + work with code simultaneously
- Uses 15% context for map, 85% for work
- No context window exhaustion
