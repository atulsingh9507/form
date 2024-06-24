import sqlite3
from pathlib import Path
 
DB_FILE = Path("jobs.db").resolve()
 
def create_connection():
    conn = sqlite3.connect(str(DB_FILE))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullName TEXT,
                    phone TEXT,
                    email TEXT,
                    resumePath TEXT,
                    address TEXT,
                    position TEXT,
                    gender TEXT,
                    qualification TEXT,
                    reference TEXT
                )''')
    conn.commit()
    return conn
 
