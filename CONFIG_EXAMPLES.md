# HenryCat Configuration Examples

This document provides examples for different use cases of HenryCat.

## 📋 Table of Contents
- [Example 1: Original Setup (E: Drive)](#example-1-original-setup-e-drive)
- [Example 2: Portable Installation](#example-2-portable-installation)
- [Example 3: Custom Media Library](#example-3-custom-media-library)
- [Example 4: Multi-Directory Scan](#example-4-multi-directory-scan)

---

## Example 1: Original Setup (E: Drive)

**Use case:** You want to catalog files on your E: drive with specific folders.

**.env configuration:**
```env
# Scan the entire E: drive
SCAN_ROOT_PATH=E:/

# Scan these specific folders
SCAN_DIRECTORIES=CURSOS,Libros,INSTALADORES

# Store database and assets in the project folder
DATABASE_PATH=./data/catalog.db
ASSETS_PATH=./assets
```

---

## Example 2: Portable Installation

**Use case:** You cloned HenryCat to any folder and want to catalog files in parent directory.

**.env configuration:**
```env
# Leave empty to scan parent directory of HenryCat installation
SCAN_ROOT_PATH=

# Scan any folders that exist in parent directory
SCAN_DIRECTORIES=Documents,Downloads,Videos

DATABASE_PATH=./data/catalog.db
ASSETS_PATH=./assets
```

**Directory structure:**
```
/home/user/
├── HenryCat/          ← Project installed here
├── Documents/         ← Will be scanned
├── Downloads/         ← Will be scanned
└── Videos/            ← Will be scanned
```

---

## Example 3: Custom Media Library

**Use case:** You have a specific media library folder.

**.env configuration:**
```env
# Point to your media library
SCAN_ROOT_PATH=/home/user/MediaLibrary

# Or on Windows:
# SCAN_ROOT_PATH=C:/Users/YourName/MediaLibrary

# Scan these categories
SCAN_DIRECTORIES=Movies,Series,Courses,Books,Software

DATABASE_PATH=./data/catalog.db
ASSETS_PATH=./assets
```

---

## Example 4: Multi-Directory Scan

**Use case:** You want to scan multiple unrelated directories.

**Option A: Scan from a common parent**

**.env configuration:**
```env
SCAN_ROOT_PATH=C:/Users/YourName

# Scan multiple folders
SCAN_DIRECTORIES=Documents/Courses,Downloads,Desktop/Projects

DATABASE_PATH=./data/catalog.db
ASSETS_PATH=./assets
```

**Option B: Use symbolic links (Advanced)**

Create symbolic links to centralize your files:

**Linux/Mac:**
```bash
mkdir ~/MyLibrary
ln -s /path/to/courses ~/MyLibrary/Courses
ln -s /path/to/books ~/MyLibrary/Books
```

**Windows (Run as Administrator):**
```cmd
mklink /D C:\MyLibrary\Courses "D:\Original\Courses"
mklink /D C:\MyLibrary\Books "E:\Original\Books"
```

**.env configuration:**
```env
SCAN_ROOT_PATH=C:/MyLibrary
SCAN_DIRECTORIES=Courses,Books

DATABASE_PATH=./data/catalog.db
ASSETS_PATH=./assets
```

---

## 🔧 Configuration Tips

### Relative vs Absolute Paths

- **Relative paths** (recommended for portability):
  ```env
  DATABASE_PATH=./data/catalog.db
  ASSETS_PATH=./assets
  ```

- **Absolute paths** (use when you want fixed locations):
  ```env
  DATABASE_PATH=/var/lib/henrycat/catalog.db
  ASSETS_PATH=/var/lib/henrycat/assets
  ```

### Path Formats

**Windows:**
- ✅ `C:/Users/Name/Documents` (forward slashes)
- ✅ `C:\\Users\\Name\\Documents` (escaped backslashes)
- ❌ `C:\Users\Name\Documents` (single backslashes - will cause errors)

**Linux/Mac:**
- ✅ `/home/username/media`
- ✅ `~/Documents` (home directory shorthand)

### Directory Names with Spaces

Always quote paths with spaces in your configuration:
```env
SCAN_ROOT_PATH="C:/Program Files/Media Library"
```

Or use escape characters:
```env
SCAN_ROOT_PATH=C:/Program\ Files/Media\ Library
```

---

## 🚀 Quick Start for Different Platforms

### Windows
```env
SCAN_ROOT_PATH=C:/Users/YourName/Documents
SCAN_DIRECTORIES=Courses,Books,Downloads
```

### Linux
```env
SCAN_ROOT_PATH=/home/username/media
SCAN_DIRECTORIES=videos,books,software
```

### macOS
```env
SCAN_ROOT_PATH=/Users/username/Documents
SCAN_DIRECTORIES=Courses,Books,Applications
```

---

## 📝 Notes

1. **Case Sensitivity**: 
   - Windows paths are case-insensitive
   - Linux/Mac paths are case-sensitive

2. **Directory Existence**: 
   - HenryCat will skip directories that don't exist
   - No error will be thrown for missing directories

3. **Performance**: 
   - Scanning large directories may take time
   - Start with smaller directories to test

4. **Updates**: 
   - After changing `.env`, restart the application
   - Re-run the "Sincronizar" button to re-scan

---

For more information, see the main [README.md](README.md)
