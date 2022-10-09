from setup import db

def get_all_novels():
    sql = "SELECT id, name FROM novels ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_novel(name : str, author_id : int, synopsis : str) -> int:
    sql = "INSERT INTO novels (name, synopsis, author_id) VALUES (:name, :synopsis, :author_id) RETURNING id"
    try:
        novel_id = db.session.execute(sql, {"name" : name, "synopsis" : synopsis, "author_id" : author_id}).fetchone()[0]
    except:
        return False
    db.session.commit()
    return novel_id

def get_novel_info(novel_id : int) -> list:
    sql = "SELECT n.name, n.synopsis, a.name, a.id FROM novels n, authors a WHERE n.id=:novel_id AND n.author_id=a.id"
    return db.session.execute(sql, {"novel_id" : novel_id}).fetchone()

def get_novel_tags(novel_id : int) -> list:
    sql = "SELECT t.id, t.name FROM novel_tags nt, tags t WHERE nt.novel_id=:novel_id AND t.id=nt.tag_id"
    return db.session.execute(sql, {"novel_id" : novel_id}).fetchall()

def get_novels_by_tag(tag_id : int) -> list:
    sql = "SELECT n.id, n.name FROM novel_tags nt, novels n WHERE nt.tag_id=:tag_id AND n.id=nt.novel_id"
    return db.session.execute(sql, {"tag_id" : tag_id}).fetchall()

def remove_novel(novel_id : int):
    sql = "DELETE FROM novels WHERE id=:novel_id"
    db.session.execute(sql, {"novel_id" : novel_id})
    db.session.commit()
