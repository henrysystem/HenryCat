import os
import fitz
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path

# Silenciar avisos de MuPDF
fitz.TOOLS.mupdf_display_errors(False)

class HenryBrain:
    def __init__(self, db_path="E:/CatalogManager/data/brain.faiss"):
        self.db_path = db_path
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None
        self.load_brain()

    def load_brain(self):
        if os.path.exists(self.db_path):
            try:
                self.vector_db = FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
                print("--- Cerebro cargado y listo ---")
            except: print("Aviso: Cerebro necesita entrenamiento.")

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        try:
            doc = fitz.open(pdf_path)
            # Aumentamos a 30 páginas para más detalle en libros
            for page_num in range(min(30, doc.page_count)):
                text += doc.load_page(page_num).get_text()
            doc.close()
        except: pass
        return text

    def train(self, items):
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        total = len(items)
        
        print(f"--- INICIANDO ENTRENAMIENTO PROFUNDO ({total} elementos) ---")

        for idx, item in enumerate(items):
            name, path, category = item['name'], item['path'], item['category']
            
            if (idx + 1) % 5 == 0:
                print(f"Analizando: {idx + 1}/{total} -> {name[:40]}...")

            # 1. Info básica
            documents.append(Document(page_content=f"Elemento: {name} | Tipo: {category} | Ruta: {path}", metadata={"source": path, "type": "meta"}))

            # 2. PDFs (Contenido profundo)
            if path.lower().endswith('.pdf') and os.path.exists(path):
                content = self.extract_text_from_pdf(path)
                if content:
                    splits = text_splitter.split_text(content)
                    for s in splits:
                        documents.append(Document(page_content=f"Libro: {name}\nTexto: {s}", metadata={"source": path, "type": "content"}))
            
            # 3. Carpetas (MAPEO RECURSIVO DE MÓDULOS Y VIDEOS)
            elif os.path.isdir(path):
                structure = []
                for root, dirs, files in os.walk(path):
                    rel_root = os.path.relpath(root, path)
                    if rel_root == ".": rel_root = "Raíz"
                    
                    # Solo nos interesan nombres de videos y pdfs para el mapa
                    valid_files = [f for f in files if f.lower().endswith(('.mp4', '.mkv', '.pdf', '.avi'))]
                    if valid_files:
                        structure.append(f"Módulo/Carpeta [{rel_root}]: " + ", ".join(valid_files))
                
                if structure:
                    # Dividimos el mapa de la carpeta en trozos si es muy grande
                    full_structure = f"Mapa de contenido del curso {name}:\n" + "\n".join(structure)
                    struct_splits = text_splitter.split_text(full_structure)
                    for ss in struct_splits:
                        documents.append(Document(page_content=ss, metadata={"source": path, "type": "structure"}))

        if documents:
            print("--- Construyendo red neuronal de conocimientos... ---")
            if self.vector_db: self.vector_db.add_documents(documents)
            else: self.vector_db = FAISS.from_documents(documents, self.embeddings)
            
            self.vector_db.save_local(self.db_path)
            print("--- ¡ENTRENAMIENTO PROFUNDO COMPLETADO! ---")
            return True
        return False

    def ask(self, query, k=6): # Aumentamos k para traer más contexto
        if not self.vector_db: return []
        return self.vector_db.similarity_search(query, k=k)

if __name__ == "__main__":
    brain = HenryBrain()
    print("Motor de Inteligencia Profunda HenryCat listo.")
