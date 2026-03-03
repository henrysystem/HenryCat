# 🐱 HenryCat - AI-Powered Digital Asset Manager

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange.svg)

**A high-end, Netflix-style digital asset manager with integrated AI chat capabilities**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [License](#-license)

</div>

---

## 📖 Overview

HenryCat is a modern digital asset management system designed to organize, view, and interact with your courses, books, and software catalog. Inspired by Netflix's sleek interface, it provides an intuitive way to manage your digital library with the power of AI-driven search and chat.

### ✨ Key Highlights

- **Netflix-style UI**: Beautiful, responsive interface built with Tailwind CSS and Lucide Icons
- **AI Brain**: Chat with your files using RAG (Retrieval-Augmented Generation) technology
- **Smart Categorization**: Automatic file type detection and categorization
- **Password Vault**: Securely store and auto-copy passwords for protected archives
- **Archive Liberation**: Clean drive policy - auto-delete archives after successful extraction
- **Poster Generation**: Automatically generates thumbnails for your media

---

## 🚀 Features

### 📂 File Management
- **Smart Scanner**: Automatically categorizes files by extension and content analysis
- **Priority System**: Installers > Videos > Books for intelligent organization
- **Archive Handling**: Supports RAR, ZIP, 7Z with automatic extraction
- **Poster System**: Web and local thumbnail generation

### 🧠 AI Chat System
- **RAG Technology**: Ask questions about your files and get intelligent answers
- **PDF Analysis**: Extracts and indexes content from PDFs (first 15 pages)
- **Folder Mapping**: Understands your file structure for better context
- **Gemini 1.5 Flash**: Powered by Google's latest AI model

### 🔐 Security
- **Henry Vault**: Encrypted password storage for archives
- **Auto-Clipboard**: Passwords automatically copied when needed
- **Fine-grained Access**: GitHub token with minimal permissions

### 🎨 User Interface
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode Ready**: Modern, eye-friendly interface
- **Fast Loading**: Optimized for performance
- **Intuitive Navigation**: Netflix-inspired browsing experience

---

## 🛠️ Tech Stack

### Backend
- **Python 3.14**: Core programming language
- **FastAPI**: High-performance web framework
- **SQLite**: Lightweight metadata storage
- **FAISS**: Vector store for AI embeddings

### AI & ML
- **Google Gemini 1.5 Flash**: AI synthesis and chat
- **Sentence-Transformers**: Text embeddings
- **PyMuPDF**: PDF text extraction

### Frontend
- **HTML/CSS/JavaScript**: Core web technologies
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Beautiful, consistent icons
- **React**: Component-based UI (planned)

### Tools & Libraries
- **OpenCV**: Video processing
- **rarfile/zipfile**: Archive handling
- **pyperclip**: Clipboard management

---

## 📦 Installation

### Prerequisites
- Python 3.14 or higher
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/henrysystem/HenryCat.git
cd HenryCat
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important Configuration Steps:**

Open `.env` and configure:

```env
# Set the root path to scan (or leave empty to scan parent directory)
SCAN_ROOT_PATH=/path/to/your/media

# Set directories to scan (comma-separated)
SCAN_DIRECTORIES=Courses,Books,Software

# Add your Gemini API key for AI features
GEMINI_API_KEY=your_api_key_here
```

**Configuration Examples:**
- See [CONFIG_EXAMPLES.md](CONFIG_EXAMPLES.md) for detailed examples
- Windows users: Use `SCAN_ROOT_PATH=C:/Users/YourName/Documents`
- Linux/Mac users: Use `SCAN_ROOT_PATH=/home/username/media`
- Portable: Leave `SCAN_ROOT_PATH` empty to scan parent directory

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open your browser**
```
http://localhost:8501
```

---

## 💻 Usage

### Basic Workflow

1. **Scan Your Files**: Point HenryCat to your media directory
2. **Browse Catalog**: View your organized assets in Netflix-style cards
3. **Chat with AI**: Ask questions about your files
4. **Manage Archives**: Extract and auto-delete compressed files
5. **Store Passwords**: Save passwords in Henry Vault for quick access

### Example Commands

```python
# Scan a directory
python scanner.py /path/to/your/files

# Start the web server
python app.py

# Train AI on your files
python ai_engine.py --train
```

---

## 📁 Project Structure

```
HenryCat/
├── ai_engine.py          # AI RAG system implementation
├── app.py                # FastAPI web application
├── database.py           # SQLite database operations
├── main.py               # Core application logic & Henry Vault
├── scanner.py            # File discovery and categorization
├── index.html            # Main web interface
├── assets/               # Generated posters and thumbnails
├── data/                 # Database and vector store
├── skills/               # AI agent skills
├── policies/             # Development policies
└── .env                  # Environment configuration (not in repo)
```

---

## 🏗️ Core Components

### 1. File Scanner (`scanner.py`)
- Scans directories recursively
- Categorizes files by extension
- Generates posters from web/local sources
- Priority-based organization

### 2. Henry Vault (`main.py` & `database.py`)
- Secure password storage
- Auto-copy to clipboard
- Encryption support
- Quick access integration

### 3. Archive Liberation
- Automatic extraction
- Verification of extracted content
- Clean drive policy (auto-delete after extraction)
- Multi-format support (RAR, ZIP, 7Z)

### 4. AI RAG System (`ai_engine.py`)
- PDF text extraction (first 15 pages)
- Folder structure mapping
- Vector embeddings with FAISS
- Gemini 1.5 Flash integration
- REST API for Windows compatibility

---

## 🔧 Configuration

HenryCat is **fully portable** and can be configured to scan any directory on your system.

### Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```env
# ====================================
# Path Configuration (IMPORTANT!)
# ====================================

# Root path to scan for files
# Examples:
#   Windows: C:/Users/YourName/Documents
#   Linux: /home/username/media
#   Mac: /Users/username/Documents
# Leave empty to scan parent directory of HenryCat
SCAN_ROOT_PATH=

# Directories to scan (comma-separated, relative to SCAN_ROOT_PATH)
SCAN_DIRECTORIES=Courses,Books,Software

# Assets path for generated posters
ASSETS_PATH=./assets

# Database path
DATABASE_PATH=./data/catalog.db

# ====================================
# AI Configuration
# ====================================
GEMINI_API_KEY=your_gemini_api_key_here

# Vector Store
FAISS_INDEX_PATH=./data/vectors.faiss

# ====================================
# Server Configuration
# ====================================
HOST=0.0.0.0
PORT=8501
DEBUG=False
```

### Configuration Examples

**Example 1: Scan specific drive (Windows)**
```env
SCAN_ROOT_PATH=E:/
SCAN_DIRECTORIES=CURSOS,Libros,INSTALADORES
```

**Example 2: Scan user documents**
```env
SCAN_ROOT_PATH=C:/Users/YourName/Documents
SCAN_DIRECTORIES=Courses,Books,Downloads
```

**Example 3: Portable mode (scan parent folder)**
```env
SCAN_ROOT_PATH=
SCAN_DIRECTORIES=Media,Documents,Projects
```

For more examples, see [CONFIG_EXAMPLES.md](CONFIG_EXAMPLES.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

### Commit Convention
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

---

## 📝 Roadmap

- [ ] Add user authentication
- [ ] Multi-user support
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Mobile app (React Native)
- [ ] Advanced AI features (image recognition, video analysis)
- [ ] Plugin system for extensibility
- [ ] Collaborative features (sharing, comments)
- [ ] Advanced search filters

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**HenrySystem**
- GitHub: [@henrysystem](https://github.com/henrysystem)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI capabilities
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Lucide Icons](https://lucide.dev/) - Beautiful icons
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search

---

<div align="center">

**Made with ❤️ by HenrySystem**

[⬆ Back to Top](#-henrycat---ai-powered-digital-asset-manager)

</div>
