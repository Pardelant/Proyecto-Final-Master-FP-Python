from escuela.modelos import Alumno, Asignatura, Profesor

class InterfazConsola:
    def __init__(self, sistema):
        self.sistema = sistema

    def mostrar_menu(self):
        print("\n" + "=" * 35)
        print("    GESTIÓN DEL CENTRO EDUCATIVO")
        print("=" * 35)
        print("1. Listar: Alumnos y Profesores (Polimorfismo)")
        print("2. Alta de Alumno")
        print("3. Alta de Profesor")
        print("4. Buscar usuario por DNI")
        print("5. Modificar usuario")
        print("6. Eliminar usuario o asignatura")
        print("7. Matricular Alumno")
        print("8. Calificar Asignatura")
        print("9. Guardar y Salir")
        return input("\nSeleccione una opción: ")

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu()
            
            if opcion == "1":
                usuarios = self.sistema.obtener_usuarios()
                if not usuarios:
                    print("\nNo hay usuarios registrados.")
                for u in usuarios:
                    print(f" > {u}")

            elif opcion == "2":
                print("\n--- Alta de Alumno ---")
                dni = input("DNI: ")
                nombre = input("Nombre: ")
                email = input("Email: ")
                nuevo_alu = Alumno(dni, nombre, email)
                self.sistema.agregar_usuario(nuevo_alu)
                print("Alumno registrado localmente.")

            elif opcion == "3":
                print("\n--- Alta de Profesor ---")
                dni = input("DNI: ")
                nombre = input("Nombre: ")
                email = input("Email: ")
                especialidad = input("Especialidad: ")
                nuevo_prof = Profesor(dni, nombre, email, especialidad)
                self.sistema.agregar_usuario(nuevo_prof)
                print("Profesor registrado localmente.")

            elif opcion == "4":
                dni = input("Introduce DNI a buscar: ")
                usuario = self.sistema.buscar_por_dni(dni)
                print(usuario if usuario else "Usuario no encontrado.")

            elif opcion == "5":
                dni = input("DNI del usuario a modificar: ")
                self.sistema.modificar_usuario(dni)

            elif opcion == "6":
                print("a) Eliminar usuario")
                print("b) Eliminar asignatura de alumno")
                sub = input("Opción: ")
                dni = input("DNI: ")
                if sub == "a":
                    self.sistema.eliminar_usuario(dni)
                else:
                    asig = input("Nombre de asignatura: ")
                    self.sistema.eliminar_asignatura_alumno(dni, asig)

            elif opcion == "7":
                dni = input("DNI del alumno: ")
                nombre_asig = input("Nombre de la asignatura: ")
                asig = Asignatura(nombre_asig)
                self.sistema.matricular_en_alumno(dni, asig)

            elif opcion == "8":
                dni = input("DNI del alumno: ")
                asig = input("Asignatura: ")
                try:
                    nota = float(input("Nota (0-10): "))
                    self.sistema.poner_nota(dni, asig, nota)
                except ValueError as e:
                    print(f"Error: {e}")

            elif opcion == "9":
                print("Guardando datos en BD...")
                self.sistema.guardar_datos()
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida.")

