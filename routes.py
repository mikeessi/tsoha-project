from flask import render_template, redirect, request
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
    return render_template("error.html", page="index", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 5 or len(username) > 12:
            return render_template("error.html", page="register", message="Tunnuksen tulee olla 5-12 merkkiä pitkä.")
        if not users.check_username(username):
            return render_template("error.html", page="register", message="Käyttäjänimi varattu")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", page="register", message="Salasanat eivät täsmää")
        if password1 == "":
            return render_template("error.html", page="register", message="Salasana ei saa olla tyhjä")
        user_role = request.form["user_role"]
        if user_role not in ["1", "2"]:
            return render_template("error.html", page="register", message="Epäkelpo käyttärooli")
        if not users.create_account(username, password1, user_role):
            return render_template("error.html", page="register", message="Rekisteröinti epäonnistui")
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
        users.check_csrf_token(request.form["csrf_token"])
        gym_name = request.form["gym_name"]
        address = request.form["address"]
        creator_id = users.get_user_id()
        if not gyms.check_gym_name(gym_name):
            return render_template("error.html", page="add_gym", message="Salin nimi varattu")
        if len(gym_name) < 2 or len(gym_name) > 30:
            return render_template("error.html", page="add_gym", message="Nimen täytyy olla 2-30 merkkiä pitkä")
        if len(address) > 30:
            return render_template("error.html", page="add_gym", message="Osoite saa olla korkeintaan 30 merkkiä pitkä")
        if not address:
            return render_template("error.hetml", page="add_gym", message="Lisää salin osoite")
        if not gyms.add_new_gym(gym_name, address, creator_id):
            return render_template("error.html", page="add_gym", message="Salin lisäys epäonnistui")
    return redirect("/gyms")

@app.route("/gyms/<int:gym_id>")
def gym_info(gym_id):
    users.check_user_access(1)
    return render_template("gym_info.html", gym_info=gyms.get_gym_info(gym_id))

@app.route("/gyms/<int:gym_id>/add_wall", methods=["POST","GET"])
def add_wall(gym_id):
    users.check_gym_ownership(gyms.get_creator_id(gym_id))
    if request.method == "GET":
        return render_template("add_wall.html", gym_id=gym_id)
    if request.method == "POST":
        users.check_csrf_token(request.form["csrf_token"])
        wall_name = request.form["wall_name"]
        wall_description = request.form["wall_description"]
        if gyms.check_wall(gym_id, wall_name):
            return render_template("error.html", page="add_wall", message="Seinä on jo olemassa")
        if len(wall_name) < 1 or len(wall_name) > 20:
            return render_template("error.html", page="add_wall", message="Seinän nimi täytyy olla 1-20 merkkiä pitkä")
        if len(wall_description) < 1 or len(wall_description) > 20:
            return render_template("error.html", page="add_wall", message="Seinän kuvauksen täytyy olla 1-20 merkkiä pitkä")
        if not gyms.add_new_wall(wall_name, wall_description, gym_id):
            return render_template("error.html", page="add_wall", message="Seinän lisäys epäonnistui")
    return redirect(f"/gyms/{gym_id}")
