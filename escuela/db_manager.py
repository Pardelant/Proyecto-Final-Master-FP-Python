import mysql
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
            hosts=c["host"],
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
            print("Error SQL: {e}")
            return None

    def listar(self, tabla):
        tablas_validas = [
            "alumnos",
            "profesores",
            "asignaturas",
            "notas_alumno",
            "asignaturas_profesores",
        ]

        if tabla not in tablas_validas:
            raise ValueError("Tabla no válida")

        self.cursor.execute(f"SELECT * FROM {tabla}")
        columnas = [desc[0] for desc in self.cursor.description]
        datos = self.cursor.fetchone()
        return tabulate(columnas, datos)

    def eliminar(self, tabla, identificador):
        tablas_validas = {
            "alumnos": "dni",
            "profesores": "dni",
            "asignaturas": "nombre",
            "notas_alumno": "id",
            "asignaturas_profesores": "profesor_id",
        }

        if tabla not in tablas_validas:
            raise ValueError("Tabla no válida")

        identificador_columna = tablas_validas[tabla]

        self.cursor.execute(
            f"DELETE FROM {tabla} WHERE {identificador_columna} = %s",
            (identificador_columna),
        )

        self.conn.commit()
        print(self.cursor.rowcount, "filas eliminadas")

    def buscar_alumno(self, dni):
        self.cursor.execute("SELECT * FROM alumnos WHERE dni = %s", (dni))
        return self.cursor.fetchone()

    def buscar_profesor(self, tabla, dni):
        self.cursor.execute("SELECT * FROM profesores WHERE dni = %s", (dni))
        return self.cursor.fetchone()

    def insertar_alumno(self, dni, nombre, email):
        self.cursor.execute(
            "INSERT into alumnos (dni, nombre, email)VALUES(%s,%s,%s)",
            (dni, nombre, email),
        )

        self.conn.commit()

        print(self.cursor.rowcount, "filas insertadas")

    def insertar_profesor(self, dni, nombre, email, especialidad):
        self.cursor.execute(
            "INSERT into profesores (dni, nombre, email,especialidad)VALUES(%s,%s,%s,%s)",
            (dni, nombre, email, especialidad),
        )

        self.conn.commit()

        print(self.cursor.rowcount, "filas insertadas")

    def insertar_asignatura(self, nombre):
        self.cursor.excute(
            "INSERT into asignaturas (nombre) VALUES (%s)", (nombre)
        )

        self.conn.commit()

        print(self.cursor.rowcount, "filas insertadas")
