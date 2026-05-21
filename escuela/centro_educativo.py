class CentroEducativo:
    def __init__(self, db_manager):
        self.db = db_manager

    def obtener_usuarios(self):
        alumnos = self.db.listar_alumnos()
        profes = self.db.listar_profesores()

        return {"alumnos": alumnos, "profesores": profes}

    def agregar_usuario(self, usuario):
        if usuario["rol"] == "alumno":
            self.db.insertar_alumno(usuario["dni"], usuario["nombre"], usuario["email"])
        elif usuario["rol"] == "profesor":
            self.db.insertar_profesor(
                usuario["dni"],
                usuario["nombre"],
                usuario["email"],
                usuario["especialidad"],
            )

    def buscar_por_dni(self, dni):

        alumno = self.db.buscar_alumno(dni)
        if alumno:
            alumno["notas_alumno"] = self.db.buscar_notas_por_alumno(dni)

            alumno["asignaturas"] = [
                a["asignatura_nombre"] for a in self.db.buscar_asignaturas_alumno(dni)
            ]

            alumno["rol"] = "alumno"
            return alumno

        profesor = self.db.buscar_profesor(dni)
        if profesor:
            profesor["asignaturas_impartidas"] = [
                self.db.buscar_asignaturas_profesor(dni)
            ]

            profesor["rol"] = "profesor"
            return profesor

        return None

    def eliminar_usuario(self, dni):
        self.db.eliminar("alumnos", dni)
        self.db.eliminar("profesores", dni)

    def eliminar_asignatura_alumno(self, dni, nombre_asig):
        self.db.eliminar_asignatura_alumno(dni, nombre_asig)

    def matricular_en_alumno(self, dni, nombre_asignatura):
        self.db.insertar_nota_alumno(dni, nombre_asignatura, 0)

    def poner_nota(self, dni, nombre_asig, nota):
        if not (0 <= nota <= 10):
            raise ValueError("La nota debe estar entre 0 y 10")

        self.db.insertar_nota_alumno(dni, nombre_asig, nota)

    def guardar_datos(self):
        print("Sincronizando cambios finales con la base de datos...")
