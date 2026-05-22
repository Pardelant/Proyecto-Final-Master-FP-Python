from escuela.modelos import Alumno, Profesor


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
        # 1. Buscamos los datos básicos del alumno
        res = self.db.buscar_alumno(dni)
        if res:
            # 2. Buscamos sus notas en la base de datos
            notas = self.db.buscar_notas_por_alumno(dni)
            # 3. Las inyectamos en el diccionario con la clave exacta que espera modelos.py
            res["notas_alumno"] = notas
            # 4. Ahora sí, creamos el objeto
            return Alumno.from_dict(res)

        # (Haz lo mismo para el profesor)
        res_prof = self.db.buscar_profesor(dni)
        if res_prof:
            asigs = self.db.buscar_asignaturas_profesor(dni)
            res_prof["asignaturas_impartidas"] = asigs
            return Profesor.from_dict(res_prof)

        return None

    def obtener_alumnos_objetos(self):
        datos_crudos = self.db.listar_alumnos()

        lista_objetos = []

        if datos_crudos:
            for fila in datos_crudos:
                dni = fila[0]

                alumno_obj = self.buscar_por_dni(dni)

                if alumno_obj:
                    lista_objetos.append(alumno_obj)

        return lista_objetos

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
