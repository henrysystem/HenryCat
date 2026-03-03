---
name: python-pandas
description: >
  Efficient data manipulation with Pandas.
  Trigger: When using 'import pandas', reading CSVs, or transforming dataframes.
metadata:
  author: dynasif
  version: "1.0"
---

## Core Rules

### ALWAYS
- Use **Vectorization** instead of loops (it's 100x faster).
- Use **Method Chaining** for cleaner transformations:
  ```python
  (df.query("age > 18")
     .assign(status="adult")
     .drop(columns=["temp"]))
  ```
- Define `dtypes` when reading large files to save memory.

### NEVER
- Loop over rows with `iterrows()` (unless absolutely necessary).
- Use `inplace=True` (deprecated/discouraged practice).
- Chain indexing assignments (`df[mask]['col'] = 1` -> SettingWithCopyWarning). Use `df.loc[mask, 'col'] = 1`.

## Examples

### Efficient Filtering
```python
# Bad
for i, row in df.iterrows():
    if row['val'] > 0: ...

# Good
df_filtered = df[df['val'] > 0]
```
