from setup import db

def add_review(creator_id : int, novel_id :int, rating : int, content : str):
    sql = """INSERT INTO review (creator_id, novel_id, rating, content, created_at) 
        VALUES (:creator_id, :novel_id, :rating, :content, now())"""
    db.session.execute(sql, {"creator_id" : creator_id, "novel_id" : novel_id, "rating" : rating, "content" : content})
    db.session.commit()

def delete_review(review_id : int):
    sql = "DELETE FROM review WHERE id=:review_id"
    db.session.execute(sql, {"review_id" : review_id})
    db.session.commit()

def get_reviews_by_user(user_id : int) -> list:
    sql = "SELECT n.name, n.id, r.content, r.rating FROM novels n, review r WHERE r.creator_id=:user_id AND n.id=r.novel_id"
    return db.session.execute(sql, {"user_id" : user_id})
