from app import db

def login(name, password):
    sql = "SELECT password, id, user_role FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":name})
    user = result.fetchone()
    if not user:
        return False
    if user[0] != password:
        return False
    return True
