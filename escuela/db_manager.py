import mysql.connector
import tabulate


class DBManager:
    def __init__(self, config):
        self.motor = config["motor"].lower()
        self.conn = None
        self.cursor = None

        self.p = "%s"
        self._conectar(config)

    def _conectar(self, c):
        self.conn = mysql.connector.connect(
            host=c["host"],
            port=c["port"],
            user=c["user"],
            password=c["pass"],
            database=c["db"],
        )

        self.cursor = self.conn.cursor()

    def ejecutar_consulta(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            if self.cursor.description:
                cols = [d[0] for d in self.cursor.description]
                return cols, self.cursor.fetchall()
        except Exception as e:
            print(f"Error SQL: {e}")
            return None

    def listar(self, tabla):
        tablas_validas = [
            "alumnos",
            "profesores",
            "asignaturas",
            "notas_alumnos",
            "asignaturas_profesores",
        ]

        if tabla not in tablas_validas:
            raise ValueError("Tabla no válida")

        self.cursor.execute(f"SELECT * FROM {tabla}")
        columnas = [desc[0] for desc in self.cursor.description]
        datos = self.cursor.fetchall()

        return tabulate.tabulate(datos, headers=columnas)

    def eliminar(self, tabla, identificador):
        tablas_validas = {
            "alumnos": "dni",
            "profesores": "dni",
            "asignaturas": "nombre",
            "notas_alumnos": "id",
            "asignaturas_profesores": "profesor_dni",
        }

        if tabla not in tablas_validas:
            raise ValueError("Tabla no válida")

        identificador_columna = tablas_validas[tabla]

        self.cursor.execute(
            f"DELETE FROM {tabla} WHERE {identificador_columna} = %s", (identificador,)
        )

        self.conn.commit()
        print(self.cursor.rowcount, "filas eliminadas")

    def buscar_alumno(self, dni):
        # Creamos un cursor temporal que devuelva diccionarios
        cursor_dict = self.conn.cursor(dictionary=True)
        cursor_dict.execute("SELECT * FROM alumnos WHERE dni = %s", (dni,))
        resultado = cursor_dict.fetchone()
        cursor_dict.close()
        return resultado

    def buscar_profesor(self, dni):
        cursor_dict = self.conn.cursor(dictionary=True)
        cursor_dict.execute("SELECT * FROM profesores WHERE dni = %s", (dni,))
        resultado = cursor_dict.fetchone()
        cursor_dict.close()
        return resultado

    def buscar_usuario(self, dni):
        cursor_dict = self.conn.cursor(dictionary=True)
        cursor_dict.execute("SELECT * FROM usuarios WHERE dni = %s", (dni,))
        resultado = cursor_dict.fetchone()
        cursor_dict.close()
        return resultado

    def insertar_alumno(self, dni, nombre, email):
        self.cursor.execute(
            "INSERT INTO alumnos (dni, nombre, email) VALUES (%s, %s, %s)",
            (dni, nombre, email),
        )

        self.conn.commit()
        print(self.cursor.rowcount, "filas insertadas")

    def insertar_profesor(self, dni, nombre, email, especialidad):
        self.cursor.execute(
            "INSERT INTO profesores (dni, nombre, email, especialidad) VALUES (%s, %s, %s, %s)",
            (dni, nombre, email, especialidad),
        )

        self.conn.commit()
        print(self.cursor.rowcount, "filas insertadas")

    def insertar_asignatura(self, nombre):
        self.cursor.execute("INSERT INTO asignaturas (nombre) VALUES (%s)", (nombre,))

        self.conn.commit()
        print(self.cursor.rowcount, "filas insertadas")

    def insertar_nota_alumno(self, alumno_dni, asignatura_nombre, nota):
        self.cursor.execute(
            "INSERT INTO notas_alumnos (alumno_dni, asignatura_nombre, nota) VALUES (%s, %s, %s)",
            (alumno_dni, asignatura_nombre, nota),
        )

        self.conn.commit()
        print(self.cursor.rowcount, "filas insertadas")
