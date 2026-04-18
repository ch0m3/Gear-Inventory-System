from app.database import get_db

def create_item(name, price, stock):
    db = get_db()
    db.execute(
        "INSERT INTO gear (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )
    db.commit()

def get_items():
    db = get_db()
    return db.execute("SELECT * FROM gear").fetchall()

def get_item(id):
    db = get_db()
    return db.execute(
        "SELECT * FROM gear WHERE id = ?",
        (id,)
    ).fetchone()

def update_item_db(id, name, price, stock):
    db = get_db()
    db.execute(
        "UPDATE gear SET name=?, price=?, stock=? WHERE id=?",
        (name, price, stock, id)
    )
    db.commit()

def delete_item_db(id):
    db = get_db()
    db.execute("DELETE FROM gear WHERE id=?", (id,))
    db.commit()