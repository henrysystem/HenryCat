import os
import json
import sqlite3
import cv2
import requests
import fitz  # PyMuPDF
import re
from pathlib import Path
from ddgs import DDGS
import time
from PIL import Image, ImageDraw, ImageFont

try:
    from ddgs.http_client import HttpClient
    HttpClient._impersonates = tuple(i for i in HttpClient._impersonates if i != "chrome_109")
except:
    pass

# CATEGORIAS Y EXTENSIONES
CATEGORIES = {
    'video': ['.mp4', '.mkv', '.avi', '.mov', '.ts'],
    'books': ['.pdf', '.epub', '.mobi'],
    'installers': ['.exe', '.msi', '.iso', '.dmg', '.pkg'],
    'code': ['.py', '.cs', '.js', '.html', '.css', '.cpp', '.c'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
}

class FileScanner:
    def __init__(self, root_path=None, assets_path=None):
        """
        Initialize FileScanner with configurable paths.
        
        Args:
            root_path: Root directory to scan. If None, uses current directory.
            assets_path: Directory to store generated posters. If None, uses ./assets
        """
        if root_path is None:
            # Use current working directory if not specified
            self.root_path = Path.cwd()
        else:
            self.root_path = Path(root_path)
        
        if assets_path is None:
            # Use assets folder relative to the scanner location
            self.assets_path = Path(__file__).parent / "assets"
        else:
            self.assets_path = Path(assets_path)
        
        self.assets_path.mkdir(exist_ok=True, parents=True)
        
    def clean_name(self, name):
        name = re.sub(r'\.zip|\.rar|\.exe|\.pdf|\.mp4', '', name, flags=re.IGNORECASE)
        name = re.sub(r'v\d+\.?\d*|v\s?\d+', '', name, flags=re.IGNORECASE)
        name = re.sub(r'20\d{2}', '', name)
        name = re.sub(r'[\._\-]', ' ', name)
        return re.sub(r'\s+', ' ', name).strip()

    def get_video_thumbnail(self, video_path, output_path):
        if output_path.exists():
            return True

        try:
            cap = cv2.VideoCapture(str(video_path))
        except:
            return False

        try:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 10)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(str(output_path), frame)
                return True
        except:
            pass
        finally:
            cap.release()

        return False

    def get_pdf_thumbnail(self, pdf_path, output_path):
        if output_path.exists(): return True
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.3, 0.3)) # Mas pequeño aun para velocidad
            pix.save(str(output_path))
            doc.close()
            return True
        except: pass
        return False

    def get_web_poster(self, query, output_name):
        # NORMALIZAMOS el nombre del archivo para evitar caracteres raros
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', output_name)
        output_path = self.assets_path / f"{safe_name}.jpg"
        
        if output_path.exists(): return str(output_path)
        
        clean_query = self.clean_name(query)
        if not clean_query: return None

        try:
            with DDGS(timeout=10) as ddgs: # TIMEOUT para no colgarse
                results = ddgs.images(f"{clean_query} course poster", max_results=1)
                for r in results:
                    img_url = r['image']
                    response = requests.get(img_url, timeout=5)
                    if response.status_code == 200:
                        with open(output_path, 'wb') as f:
                            f.write(response.content)
                        return str(output_path)
        except: pass
        return None

    def _build_search_query(self, name, category):
        clean_name = self.clean_name(name)
        if not clean_name:
            clean_name = name

        if category == 'books':
            return f"{clean_name} book cover"
        if category == 'video':
            return f"{clean_name} course cover"
        if category == 'installers':
            return f"{clean_name} software box art"
        if category == 'archives':
            return f"{clean_name} archive package"
        return f"{clean_name} cover"

    def _get_category_badge(self, category):
        badges = {
            'books': 'BOOK',
            'video': 'COURSE',
            'installers': 'SOFTWARE',
            'archives': 'ARCHIVE',
            'code': 'CODE',
            'folder': 'FOLDER',
        }
        return badges.get(category, 'ITEM')

    def _category_colors(self, category):
        palette = {
            'books': ((20, 42, 74), (13, 20, 33)),
            'video': ((70, 26, 26), (22, 12, 12)),
            'installers': ((44, 66, 26), (15, 25, 13)),
            'archives': ((67, 49, 21), (29, 20, 10)),
            'code': ((34, 41, 66), (15, 17, 27)),
            'folder': ((52, 52, 52), (20, 20, 20)),
        }
        return palette.get(category, ((52, 52, 52), (20, 20, 20)))

    def generate_fallback_poster(self, name, category, output_name):
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', output_name)
        output_path = self.assets_path / f"{safe_name}.jpg"
        if output_path.exists():
            return str(output_path)

        width, height = 800, 1200
        top_color, bottom_color = self._category_colors(category)

        try:
            img = Image.new('RGB', (width, height), color=top_color)
            draw = ImageDraw.Draw(img)

            for y in range(height):
                ratio = y / max(1, height - 1)
                r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
                g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
                b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

            try:
                title_font = ImageFont.truetype("arial.ttf", 56)
                badge_font = ImageFont.truetype("arial.ttf", 28)
            except:
                title_font = ImageFont.load_default()
                badge_font = ImageFont.load_default()

            badge_text = self._get_category_badge(category)
            draw.rounded_rectangle((40, 40, 250, 95), radius=12, fill=(255, 255, 255, 40))
            draw.text((58, 58), badge_text, fill=(230, 230, 230), font=badge_font)

            title = self.clean_name(name) or name
            title = title[:110]
            words = title.split()
            lines = []
            current = ""
            for word in words:
                test = f"{current} {word}".strip()
                if len(test) <= 28:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
            lines = lines[:4]

            y_text = 300
            for line in lines:
                draw.text((60, y_text), line, fill=(245, 245, 245), font=title_font)
                y_text += 86

            draw.rectangle((40, height - 180, width - 40, height - 130), fill=(255, 255, 255, 30))
            draw.text((60, height - 170), "CatalogManager", fill=(220, 220, 220), font=badge_font)

            img.save(output_path, format='JPEG', quality=90)
            return str(output_path)
        except:
            return None

    def get_best_poster(self, name, category, output_name):
        query = self._build_search_query(name, category)
        poster = self.get_web_poster(query, output_name)
        if poster:
            return poster
        return self.generate_fallback_poster(name, category, output_name)

    def get_poster_for_item(self, item):
        path = item.get('path', '')
        name = item.get('name', '')
        category = item.get('category', 'folder')

        if not path or not os.path.exists(path):
            return None

        if os.path.isfile(path):
            ext = Path(path).suffix.lower()
            if ext in CATEGORIES['video']:
                thumb_path = self.assets_path / f"{re.sub(r'[^a-zA-Z0-9]', '_', name)}_thumb.jpg"
                if self.get_video_thumbnail(Path(path), thumb_path):
                    return str(thumb_path)
            if ext == '.pdf':
                thumb_path = self.assets_path / f"{re.sub(r'[^a-zA-Z0-9]', '_', name)}_pdf.jpg"
                if self.get_pdf_thumbnail(path, thumb_path):
                    return str(thumb_path)
            return self.get_best_poster(name, category, name)

        # Folder case
        all_files = []
        try:
            all_files = list(Path(path).glob('**/*'))
        except:
            pass

        for f in all_files:
            if f.suffix.lower() in CATEGORIES['images'] and any(n in f.name.lower() for n in ['poster', 'cover', 'thumb', 'captura', '0.captura']):
                return str(f)

        if category == 'video':
            video_files = [f for f in all_files if f.suffix.lower() in CATEGORIES['video']]
            if video_files:
                thumb_path = self.assets_path / f"{re.sub(r'[^a-zA-Z0-9]', '_', name)}_thumb.jpg"
                if self.get_video_thumbnail(video_files[0], thumb_path):
                    return str(thumb_path)
        elif category == 'books':
            pdf_files = [f for f in all_files if f.suffix.lower() == '.pdf']
            if pdf_files:
                thumb_path = self.assets_path / f"{re.sub(r'[^a-zA-Z0-9]', '_', name)}_pdf.jpg"
                if self.get_pdf_thumbnail(str(pdf_files[0]), thumb_path):
                    return str(thumb_path)

        return self.get_best_poster(name, category, name)

    def scan_directory(self, target_dir):
        results = []
        target_path = self.root_path / target_dir
        if not target_path.exists(): return results

        for item in target_path.iterdir():
            data = {'name': item.name, 'path': str(item), 'type': 'folder' if item.is_dir() else 'file', 'category': 'folder', 'poster': None, 'files_count': 0}

            if item.is_dir():
                # Optimizamos el conteo de archivos (solo nivel superior + 1) para velocidad
                try:
                    all_files = list(item.glob('**/*')) # Limitado por la velocidad del disco
                    data['files_count'] = len(all_files)
                except: 
                    data['files_count'] = 0
                    all_files = []

                # 1. Buscar poster local
                for f in all_files:
                    if f.suffix.lower() in CATEGORIES['images'] and any(n in f.name.lower() for n in ['poster', 'cover', 'thumb', 'captura', '0.captura']):
                        data['poster'] = str(f); break
                
                # 2. Determinar categoría por extensiones
                exts = {f.suffix.lower() for f in all_files if f.is_file()}
                
                if any(ext in CATEGORIES['installers'] for ext in exts):
                    data['category'] = 'installers'
                elif any(ext in CATEGORIES['video'] for ext in exts):
                    data['category'] = 'video'
                    if not data['poster']:
                        v_files = [f for f in all_files if f.suffix.lower() in CATEGORIES['video']]
                        if v_files:
                            t_path = self.assets_path / f"{re.sub(r'[^a-zA-Z0-9]', '_', item.name)}_thumb.jpg"
                            if self.get_video_thumbnail(v_files[0], t_path): data['poster'] = str(t_path)
                elif any(ext in CATEGORIES['books'] for ext in exts):
                    data['category'] = 'books'
                    if not data['poster']:
                        p_files = [f for f in all_files if f.suffix.lower() == '.pdf']
                        if p_files:
                            t_path = self.assets_path / f"{re.sub(r'[^a-zA-Z0-9]', '_', item.name)}_pdf.jpg"
                            if self.get_pdf_thumbnail(p_files[0], t_path): data['poster'] = str(t_path)

                # 3. Web/fallback poster
                if not data['poster'] and data['files_count'] > 0:
                    data['poster'] = self.get_best_poster(item.name, data['category'], item.name)
            else:
                data['category'] = 'others'
                for cat, extensions in CATEGORIES.items():
                    if item.suffix.lower() in extensions:
                        data['category'] = cat; break
                
                if data['category'] in ['video', 'books', 'installers', 'archives', 'others']:
                    data['poster'] = self.get_best_poster(item.name, data['category'], item.name)
                
            results.append(data)
        return results
