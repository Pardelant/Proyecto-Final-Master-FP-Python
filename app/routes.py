from flask import Blueprint, render_template

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


@main.route("/")
def index():
    return render_template("index.html")