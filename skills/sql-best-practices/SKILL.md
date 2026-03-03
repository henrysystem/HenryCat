---
name: sql-best-practices
description: >
  Universal SQL best practices: normalization, indexing, capitalization, and formatting.
  Trigger: When writing any SQL query (SELECT, INSERT, UPDATE) or designing tables.
metadata:
  author: dynasif
  version: "1.0"
---

## Core Rules (ANSI SQL)

### ALWAYS
- **Capitalize Keywords**: `SELECT`, `FROM`, `WHERE` (makes reading easier).
- **Use Snake_Case**: For table and column names (`user_id`, `created_at`).
- **Format Queries**: Indent for readability.
  ```sql
  SELECT u.id, u.name
  FROM users u
  WHERE u.active = 1;
  ```
- **Use Aliases**: `FROM very_long_table_name t`.

### NEVER
- **Use `SELECT *` in Production**: Always list columns explicitly.
- **Implicit Joins**: `FROM a, b WHERE a.id = b.id`. Use `INNER JOIN` instead.
- **Commit inside loops**: Performance killer. Commit in batches.

## Indexing Basics
- Index foreign keys (`user_id` in orders table).
- Index columns used frequently in `WHERE` or `ORDER BY`.
- Don't index low-cardinality columns (e.g., boolean `is_active`) unless specifically needed for filtered indexes.
