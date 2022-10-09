from setup import db

def add_review(creator_id : int, novel_id :int, rating : int, content : str):
    sql = """INSERT INTO review (creator_id, novel_id, rating, content, created_at) 
        VALUES (:creator_id, :novel_id, :rating, :content, now())"""
    db.session.execute(sql, {"creator_id" : creator_id, "novel_id" : novel_id, "rating" : rating, "content" : content})
    db.session.commit()

