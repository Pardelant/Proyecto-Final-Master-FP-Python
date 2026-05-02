from gestion_escolar.gestion import centro_educativo


class InterfazConsola:
    def __init__(self):
        self.sistema = centro_educativo()

    def ejecutar(self):
        self.pedir_datos_alumno()

    # Bucle principal del menú
    # while not salir: ...
    def pedir_datos_alumno(self) -> dict:
        """Solicita por teclado los datos para crear un alumno"""
        dni = input("DNI: ")
        nombre = input("Nombre: ")
        email = input("EMAIL: ")
        print("ids de las asignaturas BD CD LM PROG SI")
        ids_asig = ["BD", "CD", "LM,", "PROG", "SI"]

        # ... devolver diccionario con los datos

    def mostrar_menu(self):
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Ver todos los alumnos")
        print("2. Añadir nuevo alumno")
        print("3. Ver profesores y sus asignaturas")
        print("4. Salir")
        return input("Seleccione una opción: ")
