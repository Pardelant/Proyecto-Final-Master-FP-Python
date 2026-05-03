from gestion_escolar.modelos import Alumno, Profesor, Asignatura
from gestion_escolar.ficheros import GestorFicheros

class CentroEducativo:
    def __init__(self):
        # 1. Rutas de archivos (asegúrate de que la carpeta 'datos' exista)
        self.gestor_alumnos = GestorFicheros("datos/alumno.json")
        self.gestor_profesores = GestorFicheros("datos/profesor.json")
        self.gestor_asignaturas = GestorFicheros("datos/asignatura.json")

        # 2. Carga inicial de datos usando los nombres correctos de los métodos
        datos_alu = self.gestor_alumnos.leer_json()
        datos_prof = self.gestor_profesores.leer_json()

        # 3. CORRECCIÓN: Usar from_dict para RECONSTRUIR los objetos
        self._alumnos = [Alumno.to_dict(d) for d in datos_alu]
        self._profesores = [Profesor.to_dict(d) for d in datos_prof]

    # --- MÉTODOS DE PERSISTENCIA ---
    def guardar_datos(self):
        """Guarda todas las listas en sus respectivos archivos JSON"""
        self.guardar_alumnos()
        self.guardar_profesores()
        print("Datos sincronizados en el disco duro.")

    def guardar_alumnos(self):
        lista_dicts = [a.to_dict() for a in self._alumnos]
        # CORRECCIÓN: Nombre del método según los requisitos del proyecto
        self.gestor_alumnos.guardarEnJSON(lista_dicts)

    def guardar_profesores(self):
        lista_dicts = [p.to_dict() for p in self._profesores]
        # CORRECCIÓN: Nombre del método según los requisitos del proyecto
        self.gestor_profesores.guardarEnJSON(lista_dicts)

    # --- MÉTODOS DE GESTIÓN DE USUARIOS ---
    def obtener_usuarios(self) -> list:
        """Retorna la lista combinada (Polimorfismo en acción)"""
        return self._alumnos + self._profesores

    def agregar_usuario(self, persona):
        """Añade un Alumno o Profesor a la lista correspondiente"""
        if isinstance(persona, Alumno):
            self._alumnos.append(persona)
        elif isinstance(persona, Profesor):
            self._profesores.append(persona)

    def buscar_por_dni(self, dni: str):
        """Busca en ambas listas y retorna el objeto o None"""
        for u in self.obtener_usuarios():
            if u._dni == dni: 
                return u
        return None

    def eliminar_usuario(self, dni: str):
        """Filtra las listas para eliminar al usuario por DNI"""
        self._alumnos = [a for a in self._alumnos if a._dni != dni]
        self._profesores = [p for p in self._profesores if p._dni != dni]
        print(f"Usuario con DNI {dni} eliminado del sistema.")

    def modificar_usuario(self, dni: str):
        """Busca al usuario y permite cambiar sus datos básicos"""
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
        """Busca un alumno y añade una nueva asignatura a su lista"""
        usuario = self.buscar_por_dni(dni)
        if isinstance(usuario, Alumno):
            usuario.matricular(asignatura)
            print(f"{usuario.nombre} matriculado en {asignatura.nombre}.")
        else:
            print("El DNI no corresponde a un alumno.")

    def eliminar_asignatura_alumno(self, dni: str, nombre_asig: str):
        """Busca al alumno y filtra su lista interna de asignaturas"""
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
        """Usa el método calificar() del modelo Alumno"""
        usuario = self.buscar_por_dni(dni)
        if isinstance(usuario, Alumno):
            try:
                usuario.calificar(nombre_asig, nota)
                print(f"Nota de {nombre_asig} actualizada a {nota}")
            except ValueError as e:
                print(f"Error: {e}")