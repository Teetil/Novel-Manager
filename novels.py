import string
from setup import db

def get_all_novels():
    sql = "SELECT id, name FROM novels ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_novel(name : str, author_id : int, synopsis : str) -> int:
    sql = "INSERT INTO novels (name, synopsis, author_id) VALUES (:name, :synopsis, :author_id) RETURNING id"
    novel_id = db.session.execute(sql, {"name" : name, "synopsis" : synopsis, "author_id" : author_id}).fetchone()[0]
    db.session.commit()
    return novel_id

def get_novel_info(novel_id) -> list:
    sql = "SELECT n.name, n.synopsis, a.name FROM novels n, authors a WHERE n.id=:novel_id AND n.author_id=a.id"
    return db.session.execute(sql, {"novel_id" : novel_id}).fetchone()