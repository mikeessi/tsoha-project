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
    sql = """SELECT G.id, G.name, G.address, U.name, U.id, W.name, W.description, W.id
             FROM users U, gyms G
             LEFT JOIN walls W ON G.id = W.gym_id
             WHERE G.id=:gym_id
             AND U.id = G.creator_id
             ORDER BY W.name"""
    result = db.session.execute(sql, {"gym_id":gym_id})
    data = result.fetchall()
    gym_info = data[0]
    walls = []
    for row in data:
        if row[5] is None:
            break
        walls.append((row[5],row[6],row[7]))
    return gym_info, walls

def check_wall(gym_id, wall_name):
    sql = """SELECT G.id, G.name, W.id, W.name
             FROM gyms G, walls W
             WHERE G.id = W.gym_id AND
             G.id=:gym_id AND W.name=:wall_name"""
    result = db.session.execute(sql, {"gym_id":gym_id, "wall_name":wall_name})
    wall = result.fetchone()
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

def add_boulder(routesetter_id, grade, wall_id, color):
    try:
        sql = """INSERT INTO boulders (wall_id, color, difficulty, routesetter_id)
                 VALUES (:wall_id, :color, :difficulty, :routesetter_id)"""
        db.session.execute(sql, {"wall_id":wall_id, "color":color, "difficulty":grade, "routesetter_id":routesetter_id})
        db.session.commit()
        return True
    except:
        return False

def check_gym_id(gym_id):
    sql = "SELECT id FROM gyms WHERE id=:gym_id"
    result = db.session.execute(sql, {"gym_id":gym_id})
    gym = result.fetchone()
    if gym:
        return True
    return False

def get_boulders(gym_id, grade, wall_id, boulder_id):
    sql = """SELECT G.id AS gym_id, G.name AS gym_name, W.name AS wall_name,
             B.id as boulder_id, B.difficulty AS grade, B.color AS color, U.name AS routesetter
             FROM users U, gyms G LEFT JOIN walls W ON G.id = W.gym_id
             LEFT JOIN boulders B ON B.wall_id = W.id
             WHERE (:gym_id IS NULL OR  G.id =:gym_id)
             AND (:grade IS NULL OR B.difficulty =:grade)
             AND (:wall_id IS NULL OR W.id =:wall_id)
             AND (:boulder_id IS NULL OR B.id =:boulder_id)
             AND B.routesetter_id = U.id
             ORDER BY gym_name, wall_name, grade, routesetter""" 
    result = db.session.execute(sql, {"gym_id":gym_id, "grade":grade, "wall_id":wall_id, "boulder_id":boulder_id})
    boulders = result.fetchall()
    return boulders

def get_boulder_stats(boulder_id):
    sql = """SELECT COUNT(T.user_id) AS tops FROM topped_boulders T
             WHERE T.boulder_id =:boulder_id"""
    result = db.session.execute(sql, {"boulder_id":boulder_id})
    return result.fetchone()

def get_user_status(boulder_id, user_id):
    status = {"topped":False, "project":False}
    params = {"boulder_id":boulder_id, "user_id":user_id}
    sql_top = """SELECT T.id FROM users U, topped_boulders T
                 WHERE U.id =:user_id
                 AND T.boulder_id =:boulder_id
                 AND U.id = T.user_id"""
    result = db.session.execute(sql_top, params).fetchone()
    if result:
        status["topped"] = True

    sql_project = """SELECT P.id FROM users U, projects P
                     WHERE U.id =:user_id
                     AND P.boulder_id =:boulder_id
                     AND U.id = P.user_id"""
    result = db.session.execute(sql_project, params).fetchone()
    if result:
        status["project"] = True

    return status

def delete_project(boulder_id, user_id):
    sql = """DELETE FROM projects
             WHERE user_id =:user_id AND boulder_id =:boulder_id"""
    db.session.execute(sql, {"user_id":user_id, "boulder_id":boulder_id})
    db.session.commit()

def mark_as_topped(boulder_id, user_id):
    try:
        delete_project(boulder_id, user_id)
        sql = """INSERT INTO topped_boulders (user_id, boulder_id)
                 VALUES (:user_id, :boulder_id)"""
        db.session.execute(sql, {"user_id":user_id, "boulder_id":boulder_id})
        db.session.commit()
        return True
    except:
        return False

def mark_as_project(boulder_id, user_id):
    try:
        sql = """INSERT INTO projects (user_id, boulder_id)
                 VALUES (:user_id, :boulder_id)"""
        db.session.execute(sql, {"user_id":user_id, "boulder_id":boulder_id})
        db.session.commit()
        return True
    except:
        return False

def get_topped_boulders(user_id):
    sql = """SELECT G.name AS gym_name, W.name AS wall_name,
             B.id AS boulder_id, B.difficulty AS grade, B.color AS color,
             U.name AS routesetter
             FROM users U, gyms G JOIN walls W ON G.id = W.gym_id
             JOIN boulders B ON W.id = B.wall_id
             JOIN topped_boulders T ON T.boulder_id = B.id
             JOIN users Y on Y.id = T.user_id
             WHERE Y.id =:user_id AND B.routesetter_id = U.id"""
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_projects(user_id):
    sql = """SELECT G.name AS gym_name, W.name AS wall_name,
             B.id AS boulder_id, B.difficulty AS grade, B.color AS color,
             U.name AS routesetter
             FROM users U, gyms G JOIN walls W ON G.id = W.gym_id
             JOIN boulders B ON w.id = B.wall_id
             JOIN projects P ON P.boulder_id = B.id
             JOIN users Y ON Y.id = P.user_id
             WHERE Y.id =:user_id AND B.routesetter_id = U.id"""
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
