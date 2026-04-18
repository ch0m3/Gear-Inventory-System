from app.database import get_db

def create_user(name, email, password, role):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        (name, email, password, role)
    )
    db.commit()
    return cursor.lastrowid



def find_user(email):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

def count_cms():
    db = get_db()
    result = db.execute(
        "SELECT COUNT(*) as count FROM users WHERE role = 'CM'"
    ).fetchone()
    return result["count"]