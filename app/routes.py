from flask import Blueprint, render_template, request, redirect, session, flash
from escuela.centro_educativo import CentroEducativo
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


init_sistema()


@main.route("/")
def index():
    return redirect("/login")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dni = request.form["dni"]
        password = request.form["password"]

        usuario_db = sistema.db.buscar_usuario(dni)

        if usuario_db and usuario_db["password"] == password:
            session["dni"] = usuario_db["dni"]
            session["rol"] = usuario_db["rol"]

            if usuario_db["rol"] == "profesor":
                return redirect("/profesor")

            return redirect("/alumno")

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


@main.route("/alumno")
def alumno():
    if session.get("rol") != "alumno":
        return redirect("/login")

    alumno = sistema.buscar_por_dni(session["dni"])

    todas_asignaturas = sistema.db.obtener_todas_asignaturas()

    ya_matriculado = alumno["asignaturas"]

    asignaturas_disponibles = [
        a for a in todas_asignaturas if a["nombre"] not in ya_matriculado
    ]

    return render_template(
        "alumno/dashboard.html",
        alumno=alumno,
        disponibles=asignaturas_disponibles,
        notas=alumno["notas_alumno"],  # 🔥 FIX IMPORTANTE
    )


@main.route("/profesor")
def profesor():
    if session.get("rol") != "profesor":
        return redirect("/login")

    profesor = sistema.buscar_por_dni(session["dni"])

    alumnos = [
        u for u in sistema.obtener_usuarios() if hasattr(u, "asignaturas")
    ]  # 🔥 SOLO ALUMNOS

    return render_template(
        "profesor/dashboard.html", profesor=profesor, alumnos=alumnos
    )
