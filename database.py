import sqlite3

DB_NAME = "fieldintel.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        visit_date TEXT,
        program_area TEXT,
        stakeholders TEXT,
        notes TEXT,
        photo_path TEXT,
        audio_path TEXT,
        key_findings TEXT,
        blockers TEXT,
        sentiment TEXT,
        followups TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_visit(data):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO visits(
        location,
        visit_date,
        program_area,
        stakeholders,
        notes,
        photo_path,
        audio_path,
        key_findings,
        blockers,
        sentiment,
        followups,
        tags
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)

    conn.commit()
    conn.close()


def get_all_visits():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM visits")

    rows = cursor.fetchall()

    conn.close()

    return rows