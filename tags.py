from setup import db

def add_new_tag(name : str) -> int:
    sql = "INSERT INTO tags (name) VALUES (:name) RETURNING id"
    tag_id = db.session.execute(sql, {"name" : name.lower()}).fetchone()[0]
    db.session.commit()
    return tag_id

def remove_tag(tag_id : int):
    sql = "DELETE FROM tags WHERE id=:tag_id"
    db.session.execute(sql, {"tag_id" : tag_id})
    db.session.commit()

def get_all_tags():
    sql = "SELECT id, name FROM tags ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_novel_tag(novel_id : int, tag_id : int):
    sql = "INSERT INTO novel_tags (novel_id, tag_id) VALUES (:novel_id, :tag_id)"
    db.session.execute(sql, {"novel_id" : novel_id, "tag_id" : tag_id})
    db.session.commit()