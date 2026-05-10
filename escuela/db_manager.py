import mysql


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

    # def crear(self, nobre, edad, email):

    def listar(self, tabla):
        self.cursor.excute(f"SELECT * FROM {tabla}")
        columnas = [desc[0] for desc in self.cursor.description]
        datos = self.cursor.fetchone()
        return columnas, datos
    
    # def eliminar()
    # tener encuenta las propagaciones en otras tablas

    def buscar(self, tabla, dni):
        self.cursor.excute(f"SELECT * FROM {tabla} WHERE id=%s", (dni))
        return self.cursor.fetchone()
    
    # def actualizar(self, params):
