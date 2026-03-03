---
name: config-ini
description: >
  Configuration management for dynasif.ini. Handles branch presets (Calderon, Matriz) and database connection settings.
  Trigger: When user asks to change branch, configuration, bodega, or mentions 'ini', 'sucursal', 'Calderon', 'Matriz'.
metadata:
  author: dynasif
  version: "1.0"
---

## When to Use

- When switching between branches or locations (e.g., "Cambia a Calderón").
- When modifying `dynasif.ini`.
- When user mentions "ini", "caja", "cajapos", "sucursal".

## Core Rules

1. **NEVER modify [database] section** unless explicitly requested.
2. **ALWAYS preserve formatting** (spaces, comments).
3. **ONLY modify [opciones] section**: `sucursal`, `caja`, `cajapos`.
4. **NEVER modify `empresa=1`**.

## Presets

### Bodega Calderón (CDN)
- **Sucursal**: 35
- **Caja**: 2
- **CajaPOS**: 0
- **Use case**: Testing picking, despachos, bodega logic.

### Matriz (Principal)
- **Sucursal**: 1
- **Caja**: 6
- **CajaPOS**: 4
- **Use case**: Testing billing, POS, sales.

## Examples

### Switching to Calderón
```ini
[opciones]
caja=2
cajapos=0
empresa=1
sucursal=35
```

### Switching to Matriz
```ini
[opciones]
caja=6
cajapos=4
empresa=1
sucursal=1
```
