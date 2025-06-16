import os
import sqlite3

os.makedirs("data", exist_ok=True)
path_db="data/rapport.db"
ARCHIVES_PATH="generated_docs"

def get_exported_files():
    if not os.path.exists(ARCHIVES_PATH):
        os.makedirs(ARCHIVES_PATH)

def create_table_projet():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS projets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP ) """)
    conn.commit()
    conn.close()
    
def recuperer_liste_projets():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM projets")
        projets = c.fetchall()
        return projets
    except Exception as e:
        print(e)
        
def create_table_rapport():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS rapports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            rapport_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        )
        """)
    conn.commit()
    conn.close()
    

def recuperer_liste_rapports(project_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("""
            SELECT id, title, content, rapport_date, created_at 
            FROM rapports 
            WHERE projet_id = ? 
            ORDER BY created_at DESC
        """, (project_id,))
        rapports = c.fetchall()
        return rapports
    except Exception as e:
        print(e)

def creer_table_ouvrages():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ouvrages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_ouvrage TEXT NOT NULL,
            prefecture TEXT,
            commune TEXT,
            canton TEXT,
            localite TEXT,
            numero_irh TEXT,
            nombre INTEGER,
            lieu_implantation TEXT,
            type_energie TEXT,
            type_reservoir TEXT,
            volume_reservoir REAL,
            etat TEXT,
            cause_panne TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    conn.close()


def recuperer_liste_ouvrages():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM ouvrages """)
        ouvrages = c.fetchall()
        return ouvrages
    except Exception as e:
        print(e)

def recuperer_one_ouvrages(id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM ouvrages WHERE id=?""", (id,))
        ouvrage = c.fetchone()
        des=['id','type_ouvrage', 'prefecture', 'commune', 'canton', 'localite', 'numero_irh', 'nombre',
                'lieu_implantation', 'type_energie', 'type_reservoir', 'volume_reservoir',
                'etat', 'cause_panne', 'observation','created_at']
        ouvrage=dict(zip(des, ouvrage))
        return ouvrage
    except Exception as e:
        print(e)
