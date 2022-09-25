from setup import db

def get_all_novels():
    sql = "SELECT id, name FROM novels ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_novel(name, author_id, synopsis=None):
    sql = "INSERT INTO novels (name, synopsis, author_id) VALUES (:name, :synopsis, :author_id)"
    db.session.execute(sql, {"name" : name, "synopsis" : synopsis, "author_id" : author_id})