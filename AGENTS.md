# HenryCat - Project Guidelines

## Project Overview
HenryCat is a high-end, Netflix-style digital asset manager designed to organize, view, and interact with courses, books, and software. It features an integrated AI "Brain" that allows users to chat with their local files using RAG technology.

### Tech Stack
- **Language**: Python 3.14 (Backend) / JavaScript-React (Frontend)
- **Frameworks**: FastAPI, Tailwind CSS, Lucide Icons
- **Database**: SQLite (Metadata), FAISS (Vector Store)
- **AI**: Google Gemini 1.5 Flash (Synthesis), Sentence-Transformers (Embeddings)
- **Tools**: PyMuPDF (PDFs), OpenCV (Video), rarfile/zipfile (Archives)

---

## 🛠️ Skills & Subagents Context

- **Subagents:** Use `codebase_investigator` for deep file structure analysis and `cli_help` for environment issues.
- **Memory:** Always check `SESSION_STATE.md` first. It is the single source of truth for the current dev state.

---

## 🏗️ Core Logic Reference

### 1. File Discovery (`scanner.py`)
Categorizes by extension and content analysis. Priority: Installers > Videos > Books. Generates posters from web or local thumbnails.

### 2. Henry Vault (`main.py` & `database.py`)
Stores passwords for items. On opening an archive, the password is automatically sent to the system clipboard for the user.

### 3. Archive Liberation
The app promotes a "Clean Drive" policy. When extracting archives, the original compressed file is deleted upon successful verification of the extracted folder.

### 4. AI RAG System (`ai_engine.py`)
- **Training**: Extracts text from PDFs (first 15 pages) and maps folder structures.
- **Inference**: Uses Gemini 1.5 Flash with REST transport for maximum compatibility on Windows systems.

---

## Commit Format
```text
<type>: <description>
```
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
