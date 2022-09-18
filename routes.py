from flask import render_template, redirect, request
from app import app
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return "Tervetuloa"
    return render_template("error.html")
