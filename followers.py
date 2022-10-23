from setup import db

def add_follower(user_id : int, novel_id : int):
    sql = "INSERT INTO followers (user_id, novel_id) VALUES (:user_id, :novel_id)"
    db.session.execute(sql, {"user_id" : user_id, "novel_id" : novel_id})
    db.session.commit()
    return

def remove_follower(user_id : int, novel_id : int):
    sql = "DELETE FROM followers WHERE user_id=:user_id AND novel_id=:novel_id"
    db.session.execute(sql, {"user_id" : user_id, "novel_id" : novel_id})
    db.session.commit()
    return

def get_novel_followers(novel_id : int) -> list:
    sql = "SELECT user_id FROM followers WHERE novel_id=:novel_id"
    return db.session.execute(sql, {"novel_id" : novel_id}).fetchall()

def get_user_following(user_id : int) -> list:
    sql = "SELECT novel_id, last_update_cnt FROM followers WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id" : user_id})

def update_follow_chapter(user_id : int, novel_id : int, chp_cnt : int):
    sql = "UPDATE followers SET last_update_cnt = :chp_cnt WHERE user_id=:user_id AND novel_id=:novel_id"
    db.session.execute(sql, {"user_id" : user_id, "novel_id" : novel_id, "chp_cnt" : chp_cnt})
    db.session.commit()
    return