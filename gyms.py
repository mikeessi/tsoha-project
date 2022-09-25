from db import db

def get_all_gyms():
    sql = "SELECT id, name, address FROM gyms ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_new_gym(name, address, creator_id):
    try:
        sql = """INSERT INTO gyms (name, address, creator_id) 
                 VALUES (:name, :address, :creator_id)"""
        db.session.execute(sql, {"name":name, "address":address, "creator_id":creator_id})
        db.session.commit()
        return True
    except:
        return False

def check_gym_name(gym_name):
    sql = "SELECT id, name, address FROM gyms WHERE name=:gym_name"
    result = db.session.execute(sql, {"gym_name":gym_name})
    gym = result.fetchone()
    if not gym:
        return True
    return False

def get_gym_info(gym_id):
    sql = """SELECT G.id, G.name, G.address, U.name FROM gyms G, users U 
             WHERE G.id=:gym_id AND U.id = G.creator_id"""
    result = db.session.execute(sql, {"gym_id":gym_id})
    return result.fetchone()
