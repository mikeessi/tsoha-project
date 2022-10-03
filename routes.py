from flask import render_template, redirect, request, abort
from app import app
import gyms
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
    return render_template("error.html", page="index", messages=["Väärä tunnus tai salasana"])

@app.route("/register", methods=["POST","GET"])
def register():
    errors = []
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 5 or len(username) > 12:
            errors.append("Tunnuksen täytyy olla 5-12 merkkiä pitkä")
        if not users.check_username(username):
            errors.append("Käyttäjänimi varattu")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            errors.append("Salasanat eivät täsmää")
        if password1 == "":
            errors.append("Salasana ei saa olla tyhjä")
        user_role = request.form["user_role"]
        if user_role not in ["1", "2"]:
            errors.append("Epäkelpo käyttäjärooli")
        if len(errors) > 0:
            return render_template("error.html", page="register", messages=errors)
        if not users.create_account(username, password1, user_role):
            return render_template("error.html", page="register", messages=["Rekisteröinti epäonnistui"])
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/gyms")
def gym():
    users.check_user_access(1)
    return render_template("gyms.html", gyms=gyms.get_all_gyms())

@app.route("/add_gym", methods=["POST","GET"])
def add_gym():
    users.check_user_access(2)
    if request.method == "GET":
        return render_template("add_gym.html")
    if request.method == "POST":
        errors = []
        users.check_csrf_token(request.form["csrf_token"])
        gym_name = request.form["gym_name"]
        address = request.form["address"]
        creator_id = users.get_user_id()
        if not gyms.check_gym_name(gym_name):
            errors.append("Salin nimi varattu")
        if len(gym_name) < 2 or len(gym_name) > 30:
            errors.append("Nimen täytyy olla 2-30 merkkiä pitkä")
        if len(address) > 30:
            errors.append("Osoite saa olla korkeintaa 30 merkkiä pitkä")
        if not address:
            errors.append("Lisää salin osoite")
        if len(errors) > 0:
            return render_template("error.html", page="add_gym", messages=errors)
        if not gyms.add_new_gym(gym_name, address, creator_id):
            return render_template("error.html", page="add_gym", messages=["Salin lisäys epäonnistui"])
    return redirect("/gyms")

@app.route("/gyms/<int:gym_id>")
def gym_info(gym_id):
    if not gyms.check_gym_id(gym_id):
        abort(404)
    users.check_user_access(1)
    return render_template("gym_info.html", gym_info=gyms.get_gym_info(gym_id))

@app.route("/gyms/<int:gym_id>/add_wall", methods=["POST","GET"])
def add_wall(gym_id):
    users.check_gym_ownership(gyms.get_creator_id(gym_id))
    if request.method == "GET":
        return render_template("add_wall.html", gym_id=gym_id)
    if request.method == "POST":
        errors = []
        users.check_csrf_token(request.form["csrf_token"])
        wall_name = request.form["wall_name"]
        wall_description = request.form["wall_description"]
        if gyms.check_wall(gym_id, wall_name):
            errors.append("Seinä on jo olemassa")
        if len(wall_name) < 1 or len(wall_name) > 20:
            errors.append("Seinän nimi täytyy olla 1-20 merkkiä pitkä")
        if len(wall_description) < 1 or len(wall_description) > 20:
            errors.append("Seinän kuvauksen täytyy olla 1-20 merkkiä pitkä")
        if len(errors) > 0:
            return render_template("error.html", page="add_wall", messages=errors)
        if not gyms.add_new_wall(wall_name, wall_description, gym_id):
            return render_template("error.html", page="add_wall", messages=["Seinän lisäys epäonnistui"])
    return redirect(f"/gyms/{gym_id}")

@app.route("/gyms/<int:gym_id>/add_boulder", methods=["POST","GET"])
def add_boulder(gym_id):
    users.check_user_access(2)
    if request.method == "GET":
        return render_template("add_boulder.html", gym_id=gym_id)
    if request.method == "POST":
        errors = []
        users.check_csrf_token(request.form["csrf_token"])
        routesetter_id = users.get_user_id()
        boulder_grade = request.form["grade"]
        wall_id = request.form["wall_id"]
        boulder_color = request.form["color"]
        if not boulder_grade:
            errors.append("Valitse reitin vaikeus")
        if not wall_id:
            errors.append("Valitse seinä")
        if not boulder_color:
            errors.append("Valitse reitin väri")
        if len(errors) > 0:
            return render_template("error.html", page="add_boulder", messages=errors)
        if not gyms.add_boulder(routesetter_id, boulder_grade, wall_id, boulder_color):
            return render_template("error.html", page="add_boulder", messages=["Reitin lisäys epäonnistui"])
    return redirect(f"/gyms/{gym_id}")
