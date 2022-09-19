from flask import render_template, redirect, request
from app import app
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
            return "Tervetuloa"
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

