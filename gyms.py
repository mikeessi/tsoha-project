from app import db

def get_all_gyms():
    sql = "SELECT id, name, address FROM gyms ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_new_gym(name, address):
    sql = """INSER INTO gyms (name, address) 
             VALUES (:name, :address)"""
    db.session.execute(sql, {"name":name, "address":address})
    db.session.commit()
