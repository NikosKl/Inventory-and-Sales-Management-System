from pathlib import Path
import sqlite3

base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / 'inventory.sqlite'

def get_connection():
    return sqlite3.connect(db_path)