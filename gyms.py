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
    sql = """SELECT G.id, G.name, G.address, U.name, U.id
             FROM gyms G, users U
             WHERE G.id=:gym_id AND U.id = G.creator_id"""
    result = db.session.execute(sql, {"gym_id":gym_id})
    return result.fetchone()

def check_wall(gym_id, wall_name):
    sql = """SELECT G.id, G.name, W.id, W.name
             FROM gyms G, walls W
             WHERE G.id = W.gym_id AND
             G.id=:gym_id AND W.name=:wall_name"""
    result = db.session.execute(sql, {"gym_id":gym_id, "wall_name":wall_name})
    wall = result.fetchone()
    print(wall)
    if wall:
        return True
    return False

def get_creator_id(gym_id):
    sql = "SELECT creator_id FROM gyms WHERE id=:gym_id"
    result = db.session.execute(sql, {"gym_id":gym_id})
    creator_id = result.fetchone()
    if creator_id is None:
        return None
    return creator_id[0]

def add_new_wall(wall_name, wall_description, gym_id):
    try:
        sql = """INSERT INTO walls (name, gym_id, description)
                 VALUES (:name, :gym_id, :description)"""
        db.session.execute(sql, {"name":wall_name, "gym_id":gym_id, "description":wall_description})
        db.session.commit()
        return True
    except:
        return False
