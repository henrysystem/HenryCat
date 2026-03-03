---
name: ai-bootstrap
description: >
  Instala o actualiza la estructura de IA en el proyecto actual usando el instalador central.
  Trigger: Cuando el usuario diga "instala estructura de ia", "configura agentes", o "actualiza skills".
metadata:
  author: dynasif
  version: "1.0 (Universal)"
---

## Purpose
Permitir instalacion en un paso desde cualquier proyecto, tomando el directorio actual como destino.

## Default Installer Path
- `D:/Recursos/tools/cognitive-setup/install.ps1`

## Execution Rules
- Ejecutar en el directorio actual (`-Target "."`).
- Detectar stack para seleccionar perfil por defecto:
  - PowerBuilder -> `-Profile 2`
  - Python -> `-Profile 3 -DB g`
  - Otro -> `-Profile 1`
- Si el instalador no existe, reportar error y ruta esperada.

## Recommended Command
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:/Recursos/tools/cognitive-setup/install.ps1" -Target "." -Profile auto
```
