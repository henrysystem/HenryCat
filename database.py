import sqlite3
import os

class CatalogDatabase:
    def __init__(self, db_path="E:/CatalogManager/data/catalog.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Columna password añadida a la tabla items
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    path TEXT UNIQUE NOT NULL,
                    type TEXT,
                    category TEXT,
                    subcategory TEXT,
                    poster TEXT,
                    files_count INTEGER,
                    status TEXT DEFAULT 'pending',
                    last_accessed TIMESTAMP,
                    tags TEXT,
                    password TEXT
                )
            ''')
            # Tabla para contraseñas maestras/frecuentes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS master_passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password TEXT UNIQUE NOT NULL,
                    label TEXT
                )
            ''')
            # Insertar contraseñas comunes por defecto
            common = [('www.intercambiosvirtuales.org', 'IV'), ('zentinels', 'Zentinels'), ('compucalitv', 'Compucali')]
            cursor.executemany('INSERT OR IGNORE INTO master_passwords (password, label) VALUES (?, ?)', common)
            conn.commit()

    def add_items(self, items):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for item in items:
                cursor.execute('''
                    INSERT INTO items (name, path, type, category, subcategory, poster, files_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(path) DO UPDATE SET
                        name=excluded.name, category=excluded.category, subcategory=excluded.subcategory,
                        poster=excluded.poster, files_count=excluded.files_count
                ''', (item['name'], item['path'], item['type'], item['category'], item.get('subcategory', 'Otros'), item['poster'], item['files_count']))
            conn.commit()

    def set_item_password(self, path, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE items SET password = ? WHERE path = ?', (password, path))
            conn.commit()

    def set_item_poster(self, path, poster):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE items SET poster = ? WHERE path = ?', (poster, path))
            conn.commit()

    def add_master_password(self, password, label=""):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO master_passwords (password, label) VALUES (?, ?)', (password, label))
            conn.commit()

    def get_master_passwords(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password, label FROM master_passwords')
            return cursor.fetchall()

    def get_all_items(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items ORDER BY subcategory, name')
            return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    db = CatalogDatabase()
    print("Bóveda de contraseñas activada en la base de datos.")
