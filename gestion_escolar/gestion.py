from gestion_escolar.ficheros import GestorFicheros
from gestion_escolar.modelos import Alumno


class CentroEducativo:
    def __init__(self):
        self.gestor_alumnos = GestorFicheros("alumno.json")

        datos_planos = self.gestor_alumnos.leerJSON()

        self._alumnos = [Alumno.from_dict(d) for d in datos_planos]

    def guardar_alumnos(self):

        lista_dicts = [a.to_dict() for a in self._alumnos]

        self.gestor_alumnos.guardarEnJSON(lista_dicts)
