from setup import db

def get_author_by_name(name : str) -> int:
    sql = "SELECT id FROM authors WHERE name=:name"
    return db.session.execute(sql, {"name" : name.lower()}).fetchone()

def add_new_author(name : str) -> int:
    sql = "INSERT INTO authors (name) VALUES (:name) RETURNING id"
    try:
        author_id = db.session.execute(sql, {"name" : name.lower()}).fetchone()[0]
        db.session.commit()
    except:
        return False
    return author_id

def get_author_info(author_id : int) -> list:
    sql = """SELECT a.name, n.name, n.id FROM novels n JOIN authors a ON n.author_id=a.id WHERE a.id = :author_id"""
    return db.session.execute(sql, {"author_id" : author_id}).fetchall()