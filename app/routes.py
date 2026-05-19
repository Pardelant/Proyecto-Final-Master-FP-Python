from flask import Blueprint, render_template, request, redirect, session

from escuela.gestion import CentroEducativo
from escuela.db_manager import DBManager

main = Blueprint("main", __name__)

sistema = None


def init_sistema():
    global sistema

    conf = {
        "motor": "mysql",
        "host": "localhost",
        "port": 3307,
        "user": "pardelant",
        "pass": "abc123",
        "db": "escuela-bd",
    }

    db = DBManager(conf)
    sistema = CentroEducativo(db)


# HOME
@main.route("/")
def index():
    return redirect("/login")


# LOGIN
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        dni = request.form["dni"]
        password = request.form["password"]

        usuario = sistema.db.buscar_usuario(dni)

        if usuario and usuario["password"] == password:
            session["dni"] = usuario["dni"]
            session["rol"] = usuario["rol"]

            if usuario["rol"] == "profesor":
                return redirect("/profesor")

            return redirect("/alumno")

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


# DASHBOARD PROFESOR
@main.route("/profesor")
def profesor():

    if session.get("rol") != "profesor":
        return redirect("/login")

    return render_template("profesor/dashboard.html")


# DASHBOARD ALUMNO
@main.route("/alumno")
def alumno():

    if session.get("rol") != "alumno":
        return redirect("/login")

    return render_template("alumno/dashboard.html")


# LOGOUT
@main.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
