from setup import db

def get_author_by_name(name : str) -> int:
    sql = "SELECT id FROM authors WHERE name=:name"
    return db.session.execute(sql, {"name" : name.lower()}).fetchone()

def add_new_author(name : str) -> int:
    sql = "INSERT INTO authors (name) VALUES (:name) RETURNING id"
    author_id = db.session.execute(sql, {"name" : name.lower()}).fetchone()[0]
    db.session.commit()
    return author_id

def get_author_info(author_id : int) -> list:
    sql = "SELECT a.name, n.name, n.id FROM novels n, authors a WHERE n.author_id = :author_id"
    return db.session.execute(sql, {"author_id" : author_id}).fetchall()