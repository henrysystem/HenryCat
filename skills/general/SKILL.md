---
name: python-general
description: >
  Python best practices: typing, virtual environments, project structure.
  Trigger: When writing Python code, creating scripts, or setting up environments.
metadata:
  author: dynasif
  version: "1.0"
---

## Core Rules

### ALWAYS
- Use **Type Hints** (`def func(a: int) -> str:`).
- Use **Virtual Environments** (`python -m venv .venv`).
- Follow **PEP 8** style (snake_case for functions/vars, CamelCase for classes).
- Use `if __name__ == "__main__":` for scripts.

### NEVER
- Use `import *` (wildcard imports).
- Commit `.venv` or `__pycache__` to git.
- Use mutable default arguments (`def func(a=[])`).

## Project Structure
```
project/
├── .venv/
├── src/
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```
