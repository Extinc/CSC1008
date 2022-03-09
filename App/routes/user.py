from flask import render_template
from . import routes


@routes.route("/login")
def login():
    return render_template("login.html")


@routes.route("/register")
def register():
    return render_template("register.html")
