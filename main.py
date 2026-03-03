from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from scanner import FileScanner
from database import CatalogDatabase
from ai_engine import HenryBrain
import warnings

warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
    category=UserWarning,
)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
import sqlite3
import re
import time
import threading
import shutil
import json
import zipfile
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = os.getenv("CATALOG_MANAGER_BASE_DIR", "E:/CatalogManager")
ROOT_DRIVE = os.getenv("CATALOG_MANAGER_ROOT_DRIVE", "E:/")
SYNC_DIRS = [d.strip() for d in os.getenv("CATALOG_MANAGER_SYNC_DIRS", "CURSOS,Libros,INSTALADORES,FUENTES").split(",") if d.strip()]
EXCLUDED_SYNC_DIRS = [
    d.strip().lower()
    for d in os.getenv(
        "CATALOG_MANAGER_EXCLUDED_DIRS",
        "CatalogManager,$RECYCLE.BIN,System Volume Information,RECYCLER",
    ).split(",")
    if d.strip()
]
DB_PATH = f"{BASE_DIR}/data/catalog.db"
db = CatalogDatabase(DB_PATH)
scanner = FileScanner(ROOT_DRIVE)
brain = HenryBrain()

# Variable global para el modelo de IA
llm = None
sync_lock = threading.Lock()
sync_status = {
    "status": "idle",
    "started_at": None,
    "finished_at": None,
    "last_run": None,
    "message": "",
}
MODEL_CANDIDATES = [
    os.getenv("CATALOG_MANAGER_GEMINI_MODEL", "gemini-2.0-flash"),
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash-002",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
]

class ChatQuery(BaseModel):
    message: str
    api_key: str = ""
    model: str = ""

class SyncRequest(BaseModel):
    directories: list[str] | None = None

class ModelsRequest(BaseModel):
    api_key: str

class DeleteRequest(BaseModel):
    path: str
    remove_from_catalog: bool = True

class MoveRequest(BaseModel):
    source_path: str
    destination_path: str
    update_catalog: bool = True

class PosterRefreshRequest(BaseModel):
    only_missing: bool = True

OFFICE_PREVIEW_EXTS = (".docx", ".xlsx", ".pptx")
FONT_PREVIEW_EXTS = (".ttf", ".otf", ".woff", ".woff2")

def _validate_sync_directories(directories):
    allowed_map = {}

    try:
        for entry in os.scandir(ROOT_DRIVE):
            if not entry.is_dir():
                continue
            entry_name = entry.name.strip()
            if not entry_name:
                continue
            if entry_name.lower() in EXCLUDED_SYNC_DIRS:
                continue
            allowed_map[entry_name.lower()] = entry_name
    except Exception:
        # Fallback al modo legacy si no podemos listar raiz.
        allowed_map = {name.lower(): name for name in SYNC_DIRS}

    if not directories:
        return sorted(allowed_map.values(), key=lambda x: x.lower())

    validated = []
    for directory in directories:
        normalized = directory.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key not in allowed_map:
            raise HTTPException(status_code=400, detail=f"Directorio no permitido para sync: {normalized}")
        canonical = allowed_map[key]
        if canonical not in validated:
            validated.append(canonical)
    return validated

def _is_safe_target_path(path: str):
    if not path:
        return False

    normalized_root = os.path.normcase(os.path.abspath(ROOT_DRIVE))
    normalized_base = os.path.normcase(os.path.abspath(BASE_DIR))
    normalized_target = os.path.normcase(os.path.abspath(path))

    if not normalized_target.startswith(normalized_root):
        return False

    if normalized_target in (normalized_root, normalized_base):
        return False

    return True

def _remove_path_from_catalog(path: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        like_pattern = f"{path}%"
        cursor.execute("DELETE FROM items WHERE path = ? OR path LIKE ?", (path, like_pattern))
        conn.commit()
        return cursor.rowcount

def _path_under_source(candidate_path: str, source_path: str):
    if candidate_path == source_path:
        return True
    return candidate_path.startswith(source_path + "\\") or candidate_path.startswith(source_path + "/")

def _update_catalog_paths_on_move(source_path: str, destination_path: str):
    updated_rows = 0
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, path, poster FROM items")
        rows = cursor.fetchall()

        for row in rows:
            item_id = row["id"]
            current_path = row["path"] or ""
            current_poster = row["poster"] or ""
            new_path = current_path
            new_poster = current_poster
            changed = False

            if _path_under_source(current_path, source_path):
                suffix = current_path[len(source_path):]
                new_path = destination_path + suffix
                changed = True

            if current_poster and _path_under_source(current_poster, source_path):
                suffix = current_poster[len(source_path):]
                new_poster = destination_path + suffix
                changed = True

            if changed:
                cursor.execute(
                    "UPDATE items SET path = ?, poster = ? WHERE id = ?",
                    (new_path, new_poster, item_id),
                )
                updated_rows += 1

        conn.commit()

    return updated_rows

def _normalize_text(text: str):
    return re.sub(r"\s+", " ", text or "").strip()

def _extract_docx_preview(path: str, max_chars: int = 8000):
    with zipfile.ZipFile(path, "r") as archive:
        xml_content = archive.read("word/document.xml")
    root = ET.fromstring(xml_content)
    text = _normalize_text(" ".join(root.itertext()))
    return text[:max_chars]

def _extract_pptx_preview(path: str, max_chars: int = 8000):
    with zipfile.ZipFile(path, "r") as archive:
        slide_names = sorted(
            name for name in archive.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        chunks = []
        for slide_name in slide_names[:12]:
            try:
                xml_content = archive.read(slide_name)
                root = ET.fromstring(xml_content)
                slide_text = _normalize_text(" ".join(root.itertext()))
                if slide_text:
                    chunks.append(slide_text)
            except Exception:
                continue

    text = "\n\n".join(chunks)
    return text[:max_chars]

def _extract_xlsx_preview(path: str, max_chars: int = 8000):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path, "r") as archive:
        shared_strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for si in shared_root.findall("m:si", ns):
                shared_strings.append(_normalize_text(" ".join(si.itertext())))

        worksheet_names = sorted(
            name for name in archive.namelist()
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        )
        if not worksheet_names:
            return ""

        sheet_root = ET.fromstring(archive.read(worksheet_names[0]))
        lines = []
        for row in sheet_root.findall(".//m:sheetData/m:row", ns)[:40]:
            row_values = []
            for cell in row.findall("m:c", ns):
                cell_type = cell.get("t")
                value = ""
                if cell_type == "s":
                    v_node = cell.find("m:v", ns)
                    if v_node is not None and v_node.text and v_node.text.isdigit():
                        idx = int(v_node.text)
                        if 0 <= idx < len(shared_strings):
                            value = shared_strings[idx]
                elif cell_type == "inlineStr":
                    value = _normalize_text(" ".join(cell.itertext()))
                else:
                    v_node = cell.find("m:v", ns)
                    if v_node is not None and v_node.text:
                        value = _normalize_text(v_node.text)

                if value:
                    row_values.append(value)

            if row_values:
                lines.append(" | ".join(row_values))

    text = "\n".join(lines)
    return text[:max_chars]

def _extract_office_preview(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return _extract_docx_preview(path), "docx"
    if ext == ".pptx":
        return _extract_pptx_preview(path), "pptx"
    if ext == ".xlsx":
        return _extract_xlsx_preview(path), "xlsx"
    raise ValueError("Tipo de archivo Office no soportado para preview")

def _font_characteristics_from_name(filename: str):
    lower = filename.lower()
    tags = []
    checks = [
        ("bold", "Bold"),
        ("italic", "Italic"),
        ("light", "Light"),
        ("thin", "Thin"),
        ("medium", "Medium"),
        ("black", "Black"),
        ("condensed", "Condensed"),
        ("expanded", "Expanded"),
        ("mono", "Monospace"),
        ("serif", "Serif"),
        ("sans", "Sans"),
        ("display", "Display"),
        ("script", "Script"),
    ]
    for token, label in checks:
        if token in lower and label not in tags:
            tags.append(label)
    return tags

def _font_media_url(full_path: str):
    rel_p = os.path.relpath(full_path, ROOT_DRIVE).replace("\\", "/")
    return f"/media/{rel_p}"

def _is_not_found_error(message: str):
    msg = (message or "").lower()
    return "not_found" in msg or "not found" in msg or "models/" in msg

def _is_transient_capacity_error(message: str):
    msg = (message or "").lower()
    transient_tokens = [
        "503",
        "unavailable",
        "high demand",
        "resource_exhausted",
        "rate limit",
        "429",
        "internal",
    ]
    return any(token in msg for token in transient_tokens)

def _get_model_candidates(requested_model: str = "", api_key: str = ""):
    candidates = []
    if requested_model and requested_model.strip():
        candidates.append(requested_model.strip())

    candidates.extend(MODEL_CANDIDATES)

    # Si podemos listar modelos disponibles, filtramos para evitar llamadas inválidas.
    if api_key:
        try:
            available = set(_list_available_models(api_key))
            candidates = [m for m in candidates if m in available or m == requested_model.strip()]
        except Exception:
            pass

    dedup = []
    for model_name in candidates:
        if model_name and model_name not in dedup:
            dedup.append(model_name)
    return dedup

def _invoke_with_fallback(api_key: str, requested_model: str, payload: dict, prompt: ChatPromptTemplate):
    last_error = None
    tried = []
    candidates = _get_model_candidates(requested_model, api_key)

    if not candidates:
        raise RuntimeError("No hay modelos candidatos disponibles para esta API key.")

    for model_name in candidates:
        tried.append(model_name)

        try:
            candidate_llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        except Exception as exc:
            msg = str(exc)
            last_error = exc
            if _is_not_found_error(msg):
                continue
            raise

        chain = prompt | candidate_llm

        for attempt in range(2):
            try:
                response = chain.invoke(payload)
                return response, model_name
            except Exception as exc:
                msg = str(exc)
                last_error = exc

                if _is_not_found_error(msg):
                    break

                # Reintento corto para picos temporales del proveedor.
                if _is_transient_capacity_error(msg):
                    if attempt == 0:
                        time.sleep(1.2)
                        continue
                    break

                raise

    raise RuntimeError(
        f"No fue posible generar respuesta con los modelos probados: {', '.join(tried)}. "
        f"Ultimo error: {last_error}"
    )

def _list_available_models(api_key: str):
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
    url = f"{endpoint}?{urllib.parse.urlencode({'key': api_key})}"
    request = urllib.request.Request(url, method="GET")

    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    models = payload.get("models", [])
    available = []

    for model in models:
        methods = model.get("supportedGenerationMethods", [])
        if "generateContent" not in methods:
            continue

        full_name = model.get("name", "")
        short_name = full_name.replace("models/", "") if full_name else ""
        if short_name:
            available.append(short_name)

    return sorted(set(available))

@app.post("/chat")
def chat_with_henry(query: ChatQuery):
    global llm
    
    if not query.api_key:
        return {"response": "⚠️ Henry, necesito tu Google API Key para poder procesar esta respuesta con detalle. Por favor, pégala en la configuración del chat."}

    try:
        # Buscamos contexto en nuestros archivos
        docs = brain.ask(query.message)
        if not docs:
            return {"response": "No encontré nada relacionado en tus archivos. ¿Están sincronizados y entrenados?"}

        context_text = "\n\n".join([d.page_content for d in docs])
        
        # Creamos el prompt para la IA
        prompt = ChatPromptTemplate.from_template("""
        Eres HenryCat AI, un asistente experto en la biblioteca personal de Henry. 
        Tu trabajo es responder de forma detallada y profesional basándote ÚNICAMENTE en el contexto proporcionado abajo.
        
        Contexto extraído de los archivos de Henry:
        {context}
        
        Pregunta de Henry: {question}
        
        Responde de forma útil, citando el nombre de los cursos o libros donde encontraste la información. 
        Si el contexto menciona módulos o videos específicos, diles.
        """)

        response, active_model = _invoke_with_fallback(
            query.api_key,
            query.model,
            {"context": context_text, "question": query.message},
            prompt,
        )

        return {"response": response.content, "model": active_model}
    except Exception as e:
        return {"response": f"❌ Error con la IA: {str(e)}"}

@app.post("/models")
def list_models(request: ModelsRequest):
    if not request.api_key:
        raise HTTPException(status_code=400, detail="API key requerida")

    try:
        available = _list_available_models(request.api_key)
        return {"models": available, "count": len(available)}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise HTTPException(status_code=exc.code, detail=f"Error consultando modelos: {detail}")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"No se pudo listar modelos: {str(exc)}")

@app.post("/train_ai")
def train_ai(background_tasks: BackgroundTasks):
    items = db.get_all_items()
    background_tasks.add_task(brain.train, items)
    return {"status": "training_started"}

@app.post("/sync")
def sync_catalog(request: SyncRequest | None = None):
    if not sync_lock.acquire(blocking=False):
        raise HTTPException(status_code=409, detail="Ya hay una sincronizacion en progreso")

    started_at = time.strftime("%Y-%m-%d %H:%M:%S")
    started_ts = time.time()
    sync_status.update({
        "status": "running",
        "started_at": started_at,
        "finished_at": None,
        "last_run": None,
        "message": "Sincronizando catalogo...",
    })

    try:
        target_dirs = _validate_sync_directories(request.directories if request else None)
        scanned_directories = []
        errors = []
        items_detected = 0

        for directory in target_dirs:
            try:
                items = scanner.scan_directory(directory)
                db.add_items(items)
                items_detected += len(items)
                scanned_directories.append({"directory": directory, "items": len(items)})
            except Exception as exc:
                errors.append({"directory": directory, "error": str(exc)})

        duration_seconds = round(time.time() - started_ts, 2)
        finished_at = time.strftime("%Y-%m-%d %H:%M:%S")
        status = "done" if not errors else "error"
        message = f"Sync finalizada. {items_detected} items procesados en {duration_seconds}s"

        payload = {
            "status": status,
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_seconds": duration_seconds,
            "directories": scanned_directories,
            "items_detected": items_detected,
            "items_written": items_detected,
            "errors": errors,
            "message": message,
        }
        sync_status.update({
            "status": status,
            "started_at": started_at,
            "finished_at": finished_at,
            "last_run": payload,
            "message": message,
        })
        return payload
    finally:
        sync_lock.release()

@app.post("/posters/fill_missing")
def fill_missing_posters(request: PosterRefreshRequest = PosterRefreshRequest()):
    items = db.get_all_items()
    processed = 0
    updated = 0
    failed = 0

    for item in items:
        current_poster = item.get("poster") or ""
        has_valid_poster = bool(current_poster and os.path.exists(current_poster))

        if request.only_missing and has_valid_poster:
            continue

        processed += 1
        try:
            poster = scanner.get_poster_for_item(item)
            if poster:
                db.set_item_poster(item["path"], poster)
                updated += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    return {
        "status": "ok",
        "processed": processed,
        "updated": updated,
        "failed": failed,
        "only_missing": request.only_missing,
    }

@app.get("/sync/status")
def get_sync_status():
    return sync_status

@app.get("/")
def read_root(): return FileResponse(f"{BASE_DIR}/index.html")

@app.get("/catalog")
def get_catalog():
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row
    cursor = conn.cursor(); cursor.execute('SELECT * FROM items ORDER BY subcategory, name')
    items = [dict(row) for row in cursor.fetchall()]; conn.close()
    result = []
    for item in items:
        poster_url = f"/assets/{os.path.basename(item['poster'])}" if item['poster'] and "assets" in item['poster'] else None
        if item['poster'] and not poster_url:
            try: rel_p = os.path.relpath(item['poster'], ROOT_DRIVE).replace("\\", "/"); poster_url = f"/media/{rel_p}"
            except: pass
        result.append({"id": item['id'], "name": item['name'], "path": item['path'], "category": item['category'], "subcategory": item['subcategory'], "poster": poster_url, "count": item['files_count'], "password": item['password']})
    return result

@app.get("/progress")
def get_progress(): return {"percentage": 100, "current_folder": "Listo"}

@app.get("/list_files")
def list_files(path: str):
    files = []
    valid_exts = ('.mp4', '.mkv', '.avi', '.pdf', '.exe', '.msi', '.iso', '.zip', '.rar', '.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.ttf', '.otf', '.woff', '.woff2')
    if os.path.isdir(path):
        for root, _, filenames in os.walk(path):
            for f in filenames:
                if f.lower().endswith(valid_exts):
                    try:
                        full_p = os.path.join(root, f).replace("\\", "/")
                        rel_p = os.path.relpath(full_p, ROOT_DRIVE).replace("\\", "/")
                        files.append({"name": f, "url": f"/media/{rel_p}", "full_path": full_p})
                    except: continue
    elif os.path.isfile(path):
        filename = os.path.basename(path)
        if filename.lower().endswith(valid_exts):
            try:
                full_p = path.replace("\\", "/")
                rel_p = os.path.relpath(path, ROOT_DRIVE).replace("\\", "/")
                files.append({"name": filename, "url": f"/media/{rel_p}", "full_path": full_p})
            except:
                pass
    return files

@app.get("/item_preview")
def item_preview(path: str):
    valid_exts = ('.mp4', '.mkv', '.avi', '.pdf', '.exe', '.msi', '.iso', '.zip', '.rar', '.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.ttf', '.otf', '.woff', '.woff2')
    preview_limit = 8
    preview_files = []
    preview_video_url = None

    normalized_root = os.path.abspath(ROOT_DRIVE)
    normalized_path = os.path.abspath(path)
    if not normalized_path.startswith(normalized_root):
        raise HTTPException(status_code=400, detail="Ruta fuera de la unidad permitida")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    def to_media_url(full_path: str):
        rel_p = os.path.relpath(full_path, ROOT_DRIVE).replace("\\", "/")
        return f"/media/{rel_p}"

    if os.path.isdir(path):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                if not filename.lower().endswith(valid_exts):
                    continue

                full_p = os.path.join(root, filename).replace("\\", "/")
                ext = os.path.splitext(filename)[1].lower()
                file_obj = {
                    "name": filename,
                    "full_path": full_p,
                    "url": to_media_url(full_p),
                    "ext": ext,
                }

                if preview_video_url is None and ext in ('.mp4', '.mkv', '.avi'):
                    preview_video_url = file_obj["url"]

                preview_files.append(file_obj)
                if len(preview_files) >= preview_limit:
                    break
            if len(preview_files) >= preview_limit:
                break
    else:
        filename = os.path.basename(path)
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_exts:
            file_obj = {
                "name": filename,
                "full_path": path.replace("\\", "/"),
                "url": to_media_url(path),
                "ext": ext,
            }
            preview_files.append(file_obj)
            if ext in ('.mp4', '.mkv', '.avi'):
                preview_video_url = file_obj["url"]

    return {
        "video_url": preview_video_url,
        "files": preview_files,
    }

@app.get("/office_preview")
def office_preview(path: str):
    if not _is_safe_target_path(path):
        raise HTTPException(status_code=400, detail="Ruta no permitida")
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    ext = os.path.splitext(path)[1].lower()
    if ext not in OFFICE_PREVIEW_EXTS:
        raise HTTPException(status_code=400, detail="Tipo de archivo no soportado para previsualizacion")

    try:
        preview_text, file_type = _extract_office_preview(path)
        return {
            "type": file_type,
            "path": path,
            "preview": preview_text or "No se pudo extraer texto legible de este archivo.",
        }
    except KeyError:
        raise HTTPException(status_code=422, detail="Archivo Office invalido o dañado")
    except zipfile.BadZipFile:
        raise HTTPException(status_code=422, detail="El archivo no es un Office OpenXML valido")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo generar preview: {str(exc)}")

@app.get("/font_preview_list")
def font_preview_list(path: str, text: str = "HENRY", offset: int = 0, limit: int = 120):
    if not _is_safe_target_path(path):
        raise HTTPException(status_code=400, detail="Ruta no permitida")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    safe_offset = max(0, offset)
    safe_limit = max(1, min(limit, 300))
    fonts = []
    total_fonts = 0

    def process_font_file(full_path: str):
        nonlocal total_fonts
        if not full_path.lower().endswith(FONT_PREVIEW_EXTS):
            return

        total_fonts += 1
        if total_fonts <= safe_offset or len(fonts) >= safe_limit:
            return

        filename = os.path.basename(full_path)
        ext = os.path.splitext(filename)[1].lower()
        size_bytes = 0
        try:
            size_bytes = os.path.getsize(full_path)
        except Exception:
            pass

        fonts.append(
            {
                "name": filename,
                "full_path": full_path.replace("\\", "/"),
                "url": _font_media_url(full_path),
                "ext": ext,
                "sample_text": text or "HENRY",
                "size_kb": round(size_bytes / 1024, 1) if size_bytes else 0,
                "characteristics": _font_characteristics_from_name(filename),
            }
        )

    if os.path.isfile(path):
        process_font_file(path)
    else:
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                full_p = os.path.join(root, filename)
                process_font_file(full_p)

    has_more = total_fonts > (safe_offset + len(fonts))
    return {
        "path": path,
        "text": text or "HENRY",
        "offset": safe_offset,
        "limit": safe_limit,
        "count": len(fonts),
        "total": total_fonts,
        "has_more": has_more,
        "fonts": fonts,
    }

@app.get("/open_external")
def open_external(path: str):
    if os.path.exists(path): os.startfile(path); return {"status": "opened"}
    return {"status": "error"}

@app.post("/delete_path")
def delete_path(request: DeleteRequest):
    target_path = request.path
    if not _is_safe_target_path(target_path):
        raise HTTPException(status_code=400, detail="Ruta no permitida para borrado")

    if not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    try:
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
            deleted_type = "directory"
        else:
            os.remove(target_path)
            deleted_type = "file"

        deleted_rows = 0
        if request.remove_from_catalog:
            deleted_rows = _remove_path_from_catalog(target_path)

        return {
            "status": "deleted",
            "path": target_path,
            "type": deleted_type,
            "catalog_rows_deleted": deleted_rows,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo borrar: {str(exc)}")

@app.post("/move_path")
def move_path(request: MoveRequest):
    source_path = request.source_path
    destination_path = request.destination_path

    if not _is_safe_target_path(source_path):
        raise HTTPException(status_code=400, detail="Ruta origen no permitida")

    if not _is_safe_target_path(destination_path):
        raise HTTPException(status_code=400, detail="Ruta destino no permitida")

    if not os.path.exists(source_path):
        raise HTTPException(status_code=404, detail="Ruta origen no encontrada")

    source_abs = os.path.abspath(source_path)
    destination_abs = os.path.abspath(destination_path)
    if source_abs == destination_abs:
        raise HTTPException(status_code=400, detail="Origen y destino son iguales")

    if os.path.exists(destination_path):
        raise HTTPException(status_code=409, detail="La ruta destino ya existe")

    try:
        destination_parent = os.path.dirname(destination_path)
        if destination_parent and not os.path.exists(destination_parent):
            os.makedirs(destination_parent, exist_ok=True)

        shutil.move(source_path, destination_path)
        moved_type = "directory" if os.path.isdir(destination_path) else "file"

        updated_rows = 0
        if request.update_catalog:
            updated_rows = _update_catalog_paths_on_move(source_path, destination_path)

        return {
            "status": "moved",
            "source_path": source_path,
            "destination_path": destination_path,
            "type": moved_type,
            "catalog_rows_updated": updated_rows,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo mover: {str(exc)}")

app.mount("/assets", StaticFiles(directory=f"{BASE_DIR}/assets"), name="assets")
app.mount("/media", StaticFiles(directory=ROOT_DRIVE), name="media")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
