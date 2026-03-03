import streamlit as st
import os
from scanner import FileScanner
from database import CatalogDatabase
from pathlib import Path
from PIL import Image
import subprocess

# Configuración de página estilo Netflix
st.set_page_config(page_title="Gemini Catalog", layout="wide")

# Estilos CSS Profesionales
st.markdown("""
    <style>
    .main { background-color: #141414; }
    .stApp { color: white; }
    .stButton>button {
        width: 100%; border-radius: 4px; height: 3em;
        background-color: #e50914; color: white; border: none; font-weight: bold;
    }
    .stButton>button:hover { background-color: #ff0a16; box-shadow: 0px 0px 10px #e50914; }
    .category-header {
        font-size: 28px; font-weight: bold; color: #e50914;
        margin-top: 30px; margin-bottom: 15px;
        border-left: 5px solid #e50914; padding-left: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar Base de Datos y Scanner
DB_PATH = "E:/CatalogManager/data/catalog.db"
db = CatalogDatabase(DB_PATH)
scanner = FileScanner("E:/")

# Gestión de Estado
if 'view' not in st.session_state: st.session_state.view = 'gallery'
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'search_val' not in st.session_state: st.session_state.search_val = ""

def play_in_vlc(file_path):
    os.startfile(file_path)

def show_details(item):
    st.session_state.view = 'details'
    st.session_state.selected_item = item

def render_details_view():
    item = st.session_state.selected_item
    name, path, category, poster_path = item[1], item[2], item[4], item[5]
    
    st.title(f"🎬 {name}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if poster_path and os.path.exists(poster_path):
            st.image(Image.open(poster_path), width='stretch')
        else:
            st.image("https://images.unsplash.com/photo-1522881451255-f5adad460ac3?q=80&w=400", width='stretch')
        
        if st.button("⬅️ Volver al Catálogo"):
            st.session_state.view = 'gallery'
            st.rerun()

    with col2:
        st.subheader("Contenido disponible")
        
        files = []
        if os.path.isdir(path):
            valid_exts = ['.mp4', '.mkv', '.avi', '.pdf', '.exe', '.msi']
            for root, _, filenames in os.walk(path):
                for f in filenames:
                    if any(f.lower().endswith(ext) for ext in valid_exts):
                        files.append(os.path.join(root, f))
        else:
            files = [path]

        if not files:
            st.warning("No se encontraron archivos compatibles.")
            if st.button("📁 Abrir Carpeta"): os.startfile(path)
        else:
            selected_file = st.selectbox("Selecciona un archivo:", files, format_func=lambda x: os.path.basename(x))
            
            if selected_file:
                ext = os.path.splitext(selected_file)[1].lower()
                st.markdown("---")
                
                if ext in ['.mp4', '.mkv', '.avi']:
                    # Intentar reproducir (Streamlit maneja mejor las rutas directas ahora)
                    try:
                        st.video(selected_file)
                    except:
                        st.error("Este formato de video no es compatible con el navegador.")
                    
                    if st.button("🚀 Abrir en Reproductor Externo (VLC/Sistema)"):
                        play_in_vlc(selected_file)
                
                elif ext == '.pdf':
                    if st.button("📖 Abrir Libro"): os.startfile(selected_file)
                else:
                    if st.button("⚡ Ejecutar"): os.startfile(selected_file)

def display_row(title, category_key):
    items = db.get_all_items(category_key)
    search_query = st.session_state.get('search_val', "")
    
    if search_query:
        items = [i for i in items if search_query.lower() in i[1].lower()]

    if items:
        st.markdown(f'<div class="category-header">{title}</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for idx, item in enumerate(items):
            with cols[idx % 5]:
                name, poster = item[1], item[5]
                try:
                    img = Image.open(poster) if poster and os.path.exists(poster) else "https://images.unsplash.com/photo-1522881451255-f5adad460ac3?q=80&w=400"
                    st.image(img, width='stretch')
                    st.markdown(f"<div style='height: 40px; overflow: hidden; font-size: 14px;'><b>{name}</b></div>", unsafe_allow_html=True)
                    st.button("Ver", key=f"v_{item[0]}", on_click=show_details, args=(item,))
                except:
                    st.error("Error")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.netflix.com/favicon.ico", width=40)
    st.title("Controles")
    if st.button("🏠 Inicio"):
        st.session_state.view = 'gallery'
        st.rerun()
    
    if st.button("🔄 Sincronizar"):
        with st.spinner("Escaneando..."):
            for f in ["CURSOS", "Libros", "INSTALADORES"]:
                db.add_items(scanner.scan_directory(f))
        st.success("¡Catálogo al día!")
    
    st.session_state.search_val = st.text_input("🔍 Buscar...", value=st.session_state.search_val)

# --- NAVEGACIÓN ---
if st.session_state.view == 'gallery':
    st.title("🍿 Mi Catálogo Estilo Netflix")
    display_row("🎓 Cursos y Tutoriales", "video")
    display_row("📚 Biblioteca y PDFs", "books")
    display_row("⚙️ Instaladores y Software", "installers")
    display_row("📂 Otros", "folder")
else:
    render_details_view()
