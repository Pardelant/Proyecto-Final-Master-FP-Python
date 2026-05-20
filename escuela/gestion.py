from escuela.db_manager import DBManager
from escuela.modelos import Alumno, Profesor


"""
    # PERSISTENCIA
    def guardar_datos(self):
        Guarda todas las listas en sus respectivos archivos JSON
        self.guardar_alumnos()
        self.guardar_profesores()
        print("Datos sincronizados.")

    def guardar_alumnos(self):
        lista_dicts = [a.to_dict() for a in self._alumnos]
        self.gestor_alumnos.guardar_json(lista_dicts)

    def guardar_profesores(self):
        lista_dicts = [p.to_dict() for p in self._profesores]
        self.gestor_profesores.guardar_json(lista_dicts)

    def obtener_usuarios(self) -> list:
        Retorna la lista combinada (Polimorfismo en acción)
        return self._alumnos + self._profesores

    def agregar_usuario(self, persona):
        Añade un Alumno o Profesor a la lista correspondiente
        if isinstance(persona, Alumno):
            self._alumnos.append(persona)
        elif isinstance(persona, Profesor):
            self._profesores.append(persona)

    def buscar_por_dni(self, dni: str):
        Busca en ambas listas y retorna el objeto o None
        for u in self.obtener_usuarios():
            if u._dni == dni:
                return u
        return None

    def eliminar_usuario(self, dni: str):
        Filtra las listas para eliminar al usuario por DNI
        self._alumnos = [a for a in self._alumnos if a._dni != dni]
        self._profesores = [p for p in self._profesores if p._dni != dni]
        print(f"Usuario con DNI {dni} eliminado del sistema.")

    def modificar_usuario(self, dni: str):
        Busca al usuario y permite cambiar sus datos básicos
        usuario = self.buscar_por_dni(dni)
        if not usuario:
            print("No existe usuario con ese DNI.")
            return

        print(f"Modificando a: {usuario.nombre}")
        nuevo_nombre = input("Nuevo nombre (Enter para mantener): ")
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre

        nuevo_email = input("Nuevo email (Enter para mantener): ")
        if nuevo_email:
            usuario.email = nuevo_email

        if isinstance(usuario, Profesor):
            nueva_esp = input("Nueva especialidad (Enter para mantener): ")
            if nueva_esp:
                usuario.especialidad = nueva_esp

    # --- MÉTODOS DE GESTIÓN ACADÉMICA ---
    def matricular_en_alumno(self, dni: str, asignatura: Asignatura):
        Busca un alumno y añade una nueva asignatura a su lista
        usuario = self.buscar_por_dni(dni)
        if isinstance(usuario, Alumno):
            usuario.matricular(asignatura)
            print(f"{usuario.nombre} matriculado en {asignatura.nombre}.")
        else:
            print("El DNI no corresponde a un alumno.")

    def eliminar_asignatura_alumno(self, dni: str, nombre_asig: str):
        Busca al alumno y filtra su lista interna de asignaturas
        usuario = self.buscar_por_dni(dni)
        if isinstance(usuario, Alumno):
            original_count = len(usuario._asignaturas)
            usuario._asignaturas = [
                a for a in usuario._asignaturas if a.nombre != nombre_asig
            ]
            if len(usuario._asignaturas) < original_count:
                print(f"Asignatura {nombre_asig} eliminada.")
            else:
                print("Asignatura no encontrada en el expediente.")

    def poner_nota(self, dni: str, nombre_asig: str, nota: float):
        Usa el método calificar() del modelo Alumno
        usuario = self.buscar_por_dni(dni)
        if isinstance(usuario, Alumno):
            try:
                usuario.calificar(nombre_asig, nota)
                print(f"Nota de {nombre_asig} actualizada a {nota}")
            except ValueError as e:
                print(f"Error: {e}")
"""


class CentroEducativo:
    def __init__(self, db_manager):
        self.db = db_manager

    def obtener_usuarios(self):
        usuarios = []
        # Obtenemos los datos crudos de la DB
        # Asumimos que listar devuelve (columnas, datos)
        _, alumnos_raw = self.db.listar("alumnos")
        _, profes_raw = self.db.listar("profesores")

        for a in alumnos_raw:
            usuarios.append(Alumno.from_dict(a))
        for p in profes_raw:
            usuarios.append(Profesor.from_dict(p))
        return usuarios

    # 2 3
    def agregar_usuario(self, usuario):
        if isinstance(usuario, Alumno):
            self.db.insertar_alumno(usuario.dni, usuario.nombre, usuario.email)
        elif isinstance(usuario, Profesor):
            self.db.insertar_profesor(
                usuario.dni, usuario.nombre, usuario.email, usuario.especialidad
            )

    def buscar_por_dni(self, dni):
        # Alumno
        res = self.db.buscar_alumno(dni)
        if res:
            notas = self.db.buscar_notas_por_alumno(dni)
            res["notas_alumno"] = notas
            return Alumno.from_dict(res)

        # Profesor
        res = self.db.buscar_profesor(dni)
        if res:
            asigs = self.db.buscar_asignaturas_profesor(dni)
            res["asignaturas_impartidas"] = asigs
            return Profesor.from_dict(res)

        return None

    def obtener_alumnos_objeto(self):
        cursor_dict = self.db.conn.cursor(dictionary=True)
        cursor_dict.execute("SELECT * FROM alumnos")
        filas = cursor_dict.fetchall()
        cursor_dict.close()

        alumnos = []
        for f in filas:
            notas = self.db.buscar_notas_por_alumno(f["dni"])
            f["notas_alumno"] = notas
            alumnos.append(Alumno.from_dict(f))
        return alumnos

    def modificar_usuario(self, dni):
        print(f"Función de modificación para DNI {dni} en desarrollo...")

    def eliminar_usuario(self, dni):
        self.db.eliminar("alumnos", dni)
        self.db.eliminar("profesores", dni)

    def eliminar_asignatura_alumno(self, dni, nombre_asig):
        sql = (
            "DELETE FROM notas_alumno WHERE alumno_dni = %s AND asignatura_nombre = %s"
        )
        self.db.ejecutar_consulta(sql, (dni, nombre_asig))
        print(f"Asignatura {nombre_asig} eliminada para el alumno {dni}")

    def matricular_en_alumno(self, dni, asignatura):

        self.db.insertar_nota_alumno(dni, asignatura.nombre, 0)

    def poner_nota(self, dni, nombre_asig, nota):
        if not (0 <= nota <= 10):
            raise ValueError("La nota debe estar entre 0 y 10")

        self.db.insertar_nota_alumno(dni, nombre_asig, nota)

    def guardar_datos(self):

        print("Sincronizando cambios finales con la base de datos...")
