from flask import Blueprint, render_template, request, redirect, session, flash
from escuela.centro_educativo import CentroEducativo
from escuela.db_manager import DBManager
from escuela.modelos import Asignatura

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


# Aseguramos que el sistema esté inicializado al importar el blueprint
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

    # objeto Alumno
    alumno_obj = sistema.buscar_por_dni(session["dni"])

    # Asignaturas
    todas_asignaturas = sistema.db.obtener_todas_asignaturas()

    ya_matriculado = [asig.nombre for asig in alumno_obj._asignaturas]
    asignaturas_disponibles = [
        a for a in todas_asignaturas if a["nombre"] not in ya_matriculado
    ]

    return render_template(
        "alumno/dashboard.html", alumno=alumno_obj, disponibles=asignaturas_disponibles
    )


@main.route("/alumno/matricular", methods=["POST"])
def alumno_matricular():
    if session.get("rol") != "alumno":
        return redirect("/login")

    dni = session["dni"]
    nombre_asignatura = request.form["asignatura"]

    # 1. Ejecutamos la lógica instanciando el objeto Asignatura como pide tu CentroEducativo
    nueva_asig = Asignatura(nombre_asignatura, 0.0)
    sistema.matricular_en_alumno(dni, nueva_asig)

    flash(f"Te has matriculado con éxito en {nombre_asignatura}", "success")
    return redirect("/alumno")


@main.route("/profesor")
def profesor():
    if session.get("rol") != "profesor":
        return redirect("/login")

    profesor_obj = sistema.buscar_por_dni(session["dni"])

    lista_alumnos = sistema.obtener_alumnos_objetos()

    return render_template(
        "profesor/dashboard.html", profesor=profesor_obj, alumnos=lista_alumnos
    )


@main.route("/profesor/calificar", methods=["POST"])
def profesor_calificar():
    if session.get("rol") != "profesor":
        return redirect("/login")

    alumno_dni = request.form["alumno_dni"]
    asignatura = request.form["asignatura"]

    try:
        nota = float(request.form["nota"])
        # Usamos tu validador e inserción del CentroEducativo
        sistema.poner_nota(alumno_dni, asignatura, nota)
        flash("Nota actualizada correctamente", "success")
    except ValueError as e:
        flash(f"Error al asignar nota: {e}", "danger")

    return redirect("/profesor")


@main.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
