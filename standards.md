# `techind` Code Standards

This document defines the coding standards for the `techind` library. It is intended to be read by an AI reviewer before a developer commits and pushes changes.

---

## How to Use This Document (AI Reviewer Instructions)

When asked to review staged or recently changed files in this repo:

1. Read this document in full before looking at any code.
2. Read every changed `.py` file (including `__init__.py` if modified).
3. Work through each section below as a checklist, applying every relevant rule to every changed file.
4. Report findings as **actionable feedback only** — do not make any code changes.
5. Organise your feedback by file, then by section heading from this document.
6. Distinguish clearly between:
   - 🔴 **Must fix** — violates a hard standard; should not be merged as-is.
   - 🟡 **Should fix** — best-practice issue; ideally resolved before merging.
   - 🟢 **Consider** — a suggestion or improvement that is optional.
7. If a file passes all checks cleanly, say so explicitly.
8. Do **not** comment on the mathematical correctness of indicator calculations — assume they are correct.

---

## 1. File & Module Structure

### 1.1 One function per file
Each indicator lives in its own `.py` file. A file must contain exactly one public function (the indicator). Helper functions used only within that file are acceptable, but must be prefixed with an underscore (e.g., `_find_first_non_nan`).

### 1.2 File name matches function name
The file name must exactly match the function it exports, e.g. `exponentialMovingAverage.py` exports `exponentialMovingAverage`.

### 1.3 `__init__.py` must be updated
Every new indicator function must be imported and re-exported in `techind/__init__.py`. Check that:
- The import statement is present and uses the form:
  ```python
  from techind.myIndicator import myIndicator as myIndicator
  ```
- The function name appears in the `hard_dependencies` check block if it introduces a new dependency.

### 1.4 Imports must be at the top of the file
All `import` statements must appear at the **top** of the file, before the function definition — not inside the function body. This is standard Python practice (PEP 8) and avoids repeated import overhead.

**Non-compliant example (currently present in codebase — flag in any new or edited file):**
```python
def exponentialMovingAverage(period, data):
    import numpy as np   # ← must move to top of file
```

---

## 2. Naming Conventions

### 2.1 Function names — camelCase
All indicator function names use `camelCase` (not `snake_case`). This is an intentional convention for this library.
- ✅ `exponentialMovingAverage`
- ❌ `exponential_moving_average`

### 2.2 Variable names — camelCase
Local variable names within indicator functions should also use `camelCase`, consistent with the existing codebase style.
- ✅ `firstNonNan`, `dataLength`, `smoothingConstant`
- ❌ `first_non_nan`, `data_length`

### 2.3 No single-letter variable names (except loop counters)
- Loop counter variables `i`, `j`, `m` are acceptable inside `for` loops.
- All other variables must have a descriptive camelCase name.
- ❌ `k`, `s`, `d` used as standalone variables without a comment explaining what they represent.

---

## 3. Type Hints

### 3.1 All function signatures must include type hints
Every function parameter and return value must be annotated. Use `numpy.ndarray` for array inputs/outputs and built-in types for scalars.

**Required signature pattern for a single-period, single-series indicator:**
```python
import numpy as np
from numpy import ndarray

def exponentialMovingAverage(period: int, data: ndarray) -> ndarray:
```

**For indicators with additional scalar parameters (e.g. KAMA):**
```python
def kaufmanAdaptiveMovingAverage(
    period: int,
    fastEMA: int,
    slowEMA: int,
    data: ndarray,
) -> ndarray:
```

### 3.2 Do not use `Any` or omit types on public functions
Every public function (no leading underscore) must have fully annotated parameters and return type. Missing annotations on a public function are a 🔴 Must fix.

---

## 4. Docstrings

### 4.1 Every public function must have a docstring
A docstring is required directly below the function signature (before any code). It must follow **NumPy docstring style**.

**Minimum required sections:**
- Short one-line summary.
- `Parameters` section describing each argument (name, type, description).
- `Returns` section describing the output array.
- (Optional but encouraged) `Notes` section for a brief explanation of the algorithm or a reference.

**Template:**
```python
def exponentialMovingAverage(period: int, data: ndarray) -> ndarray:
    """
    Calculate the Exponential Moving Average (EMA) of a time series.

    Parameters
    ----------
    period : int
        Number of periods to include in the EMA calculation. Must be >= 1.
    data : numpy.ndarray
        One-dimensional array of price values (e.g. daily close prices).
        May contain leading or trailing NaN values.

    Returns
    -------
    numpy.ndarray
        Array of the same length as `data`. Values before the warm-up
        period and beyond the last valid data point are set to NaN.

    Notes
    -----
    Uses the standard recursive formula:
        EMA[i] = (data[i] - EMA[i-1]) * multiplier + EMA[i-1]
    where multiplier = 2 / (period + 1).
    The first valid EMA value is seeded with the SMA of the first `period` values.
    """
```

### 4.2 Inline comments
Inline comments should explain *why*, not *what*. Do not comment on things that are self-evident from the code.

- ✅ `# Seed the recursive formula with the SMA of the first window`
- ❌ `# calculate EMA` (above a line that obviously calculates the EMA)
- ✅ Comments marking logical sections with `# ---` are acceptable and consistent with existing style.

---

## 5. Input Validation

### 5.1 Validate `period`
Every indicator must validate `period` before doing any computation. Raise a clear `ValueError` if invalid.

```python
if not isinstance(period, int) or period < 1:
    raise ValueError(f"period must be a positive integer, got {period!r}")
```

### 5.2 Validate `data`
```python
if not isinstance(data, np.ndarray):
    raise TypeError(f"data must be a numpy.ndarray, got {type(data).__name__!r}")
if data.ndim != 1:
    raise ValueError(f"data must be a 1-dimensional array, got shape {data.shape}")
if len(data) < period:
    raise ValueError(
        f"data length ({len(data)}) must be >= period ({period})"
    )
```

### 5.3 Validate extra scalar parameters
Any additional integer/float parameters (e.g. `fastEMA`, `slowEMA`) must also be validated:
- Must be of the expected type.
- Must be within a sensible range (e.g. `fastEMA < slowEMA` for KAMA).

---

## 6. Output Contract

All indicator functions must honour the following output contract:

### 6.1 Output length equals input length
`len(result) == len(data)` — always.

### 6.2 Warm-up values are `np.nan`
Positions before the indicator has enough data to produce a valid result must be `np.nan`, not `0` or any other sentinel value.

### 6.3 Trailing NaN mirroring
Positions beyond `lastNonNan` in the input must also be `np.nan` in the output. The output's valid range must not extend beyond the input's valid range.

### 6.4 Output array dtype is `float64`
Always initialise the output with:
```python
out = np.full(len(data), np.nan, dtype=np.float64)
```
(Preferred over `np.zeros(len(data))` because it avoids accidentally returning `0` instead of `NaN` in positions that were never computed.)

---

## 7. Repeated Logic

### 7.1 First/last non-NaN detection
Every indicator currently contains a copy-pasted block to find `firstNonNan` and `lastNonNan`. This is acceptable for now, but any *new* file added after the codebase extracts this into a shared helper (e.g. `techind/_utils.py`) must use the shared helper rather than copy-paste.

Until that refactor is done, the reviewer should flag copy-pasted detection blocks in new files as 🟡 Should fix (suggesting extraction), not 🔴 Must fix.

---

## 8. Tests

### 8.1 Every new indicator must have tests
Any new `.py` file added to `techind/` must have a corresponding test block in `tests/test_indicators.py`. The minimum required tests per indicator are:

| Test | What to check |
|------|---------------|
| Output length | `len(result) == len(data)` |
| Leading NaN warm-up | First `period - 1` values are `NaN` |
| No NaN after warm-up | No `NaN` values after the warm-up period (given clean input) |
| Constant series | A flat input series should produce the same constant value throughout the valid range |
| Known value | At least one hard-coded expected output value verified against a trusted source or manual calculation |

### 8.2 Test naming convention
Test function names must use `snake_case` and describe what is being tested:
```
test_ema_output_length
test_ema_leading_values_are_nan
test_ema_constant_series
```

### 8.3 No magic numbers in tests
Any `period` or seed value used in tests must be assigned to a named variable before use:
```python
PERIOD = 14
result = ti.exponentialMovingAverage(PERIOD, data)
```

---

## 9. General Python Best Practices

### 9.1 No bare `== False` / `== True` comparisons
Use `not` / truthiness instead.
- ❌ `if np.isnan(data[i]) == False:`
- ✅ `if not np.isnan(data[i]):`

### 9.2 No unused variables
Remove any variables that are assigned but never read (e.g. intermediate arrays that are computed but not returned and not used in further calculations).

### 9.3 Avoid `range(len(x))` when the index is not needed
If only the value is needed, iterate directly:
- ❌ `for i in range(len(data)): val = data[i]`
- ✅ `for val in data:`

If the index *is* needed, `enumerate` is preferred:
- ✅ `for i, val in enumerate(data):`

This is a 🟢 Consider for existing patterns and a 🟡 Should fix for newly written code.

### 9.4 Consistent spacing
Follow PEP 8 spacing rules:
- Two blank lines between top-level definitions.
- One space around binary operators.
- No trailing whitespace.

---

## 10. `__init__.py` Standards

### 10.1 Imports must be alphabetically sorted
All indicator imports in `__init__.py` should be in alphabetical order by function name.

### 10.2 `hard_dependencies` list must be accurate
The `hard_dependencies` list must include every third-party package actually used across all indicator modules. If a new indicator uses a new package (e.g. `scipy`), that package must be added to `hard_dependencies` and to `pyproject.toml`'s `dependencies`.

---

## 11. Checklist Summary for AI Reviewer

Before submitting feedback, confirm you have checked every changed file against:

- [ ] File name matches function name (§1.2)
- [ ] `__init__.py` updated (§1.3)
- [ ] All imports at top of file, not inside functions (§1.4)
- [ ] Function and variable names are camelCase (§2.1, §2.2)
- [ ] No unexplained single-letter variable names outside loop counters (§2.3)
- [ ] Type hints present on all public function signatures (§3.1, §3.2)
- [ ] NumPy-style docstring present and complete (§4.1)
- [ ] Inline comments explain *why*, not *what* (§4.2)
- [ ] `period` validation present (§5.1)
- [ ] `data` validation present (§5.2)
- [ ] Extra parameter validation present where applicable (§5.3)
- [ ] Output length equals input length (§6.1)
- [ ] Warm-up positions are `np.nan` (§6.2)
- [ ] Output array initialised with `np.full(..., np.nan)` (§6.4)
- [ ] Tests added for new indicator (§8.1)
- [ ] No `== False` / `== True` comparisons (§9.1)
- [ ] No unused variables (§9.2)
