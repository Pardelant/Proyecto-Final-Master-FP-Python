from app.interfaz_usuario import InterfazConsola
from datetime import datetime
from escuela.db_manager import DBManager

"""
from gestion_escolar.common import DatoInvalido, Validator
from gestion_escolar.gestion import centro_educativo
from gestion_escolar.modelos import Alumno, Asignatura, Profesor


def crear_profesor(datos):
    dni = datos.get("dni", "").strip()
    nombre = Validator.formatear_nombre(datos.get("nombre", ""))
    email = datos.get("email", "").strip()
    especialidad = datos.get("especialidad", "").strip()

    if not Validator.validar_dni(dni):
        raise DatoInvalido(f"DNI inválido: {dni}")

    return Profesor(dni, nombre, email, especialidad)


def crear_alumno(datos):
    dni = datos.get("dni", "").strip()
    nombre = Validator.formatear_nombre(datos.get("nombre", ""))
    email = datos.get("email", "").strip()

    if not Validator.validar_dni(dni):
        raise DatoInvalido(f"DNI inválido: {dni}")

    return Alumno(dni, nombre, email)

# def localizar(dni):



def modificar(dni):
    #metodo void para modificar json

    return True
    

def guardar_modificaciones():

    return True


def main():

    #PUNTO DE ENTRADA.

    #LLAMAR APP.INTERFAZ_USUARIO




    centro = centro_educativo()

    datos = [
        {
            "tipo": "Profesor",
            "dni": "12345678A",
            "nombre": "pepe",
            "email": "pepe@centro.edu",
            "especialidad": "Informática",
        },
        {
            "tipo": "Alumno",
            "dni": "87654321B",
            "nombre": "eva",
            "email": "eva@centro.edu",
        },
        {
            "tipo": "Alumno",
            "dni": "23456789C",
            "nombre": "jose",
            "email": "jose@centro.edu",
        },
        {
            "tipo": "Alumno",
            "dni": "1234X",
            "nombre": "invalido",
            "email": "error@centro.edu",
        },
    ]

    for persona_datos in datos:
        try:
            tipo = persona_datos.get("tipo")
            if tipo == "Profesor":
                persona = crear_profesor(persona_datos)
            elif tipo == "Alumno":
                persona = crear_alumno(persona_datos)
            else:
                raise DatoInvalido("Tipo de usuario desconocido")

            centro.agregar_usuario(persona)
        except DatoInvalido as error:
            nombre = persona_datos.get("nombre", "<sin nombre>")
            print(f"Aviso: no se pudo crear {nombre}. {error}")

    print("\nUsuarios registrados en el centro:")
    centro.listar_usuarios()

    print("\nMatriculando alumnos y asignando notas...")
    for usuario in centro.obtener_usuarios():
        if isinstance(usuario, Alumno):
            usuario.matricular(Asignatura("Python"))
            usuario.matricular(Asignatura("Bases de Datos"))
            usuario.calificar("Python", 8.5)
            usuario.calificar("Bases de Datos", 9.0)

    alumnos = [u for u in centro.obtener_usuarios() if isinstance(u, Alumno)]
    profesores = [u for u in centro.obtener_usuarios() if isinstance(u, Profesor)]

    promedio_global = (
        sum(alumno.nota_media() for alumno in alumnos) / len(alumnos)
        if alumnos
        else 0.0
    )

    print(f"\nTotal de alumnos: {len(alumnos)}")
    print(f"Total de profesores: {len(profesores)}")
    print(f"Nota media global del centro: {promedio_global:.2f}")


if __name__ == "__main__":
    main()
"""


def main():
    conf = {
        "motor": "mysql",
        "host": "localhost",
        "port": 3307,
        "user": "pardelant",
        "pass": "abc123",
        "db": "escuela-db",
    }
    db = DBManager(conf)
    """inicio"""

    while True:
        op = InterfazConsola.menu()

        if op == "1":
            res = db.ejecutar_consulta("SELECT * FROM alumnos")
            if res:
                InterfazConsola.mostrar_tabla(*res)

        elif op == "2":
            res = db.ejecutar_consulta("SELECT * FROM punto")
            if res:
                InterfazConsola.mostrar_tabla(*res)

        elif op == "3":
            # Para el registro necesitamos IDs existentes
            p_id = input("ID del Punto: ")
            m_id = input("ID del Material: ")
            cant = input("Cantidad (kg): ")
            fuente = input("Fuente (domiciliario/empresa/evento): ")
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.registro_crear(fecha, p_id, m_id, cant, fuente)
            print("Depósito registrado.")

        elif op == "4":
            res = db.listar_con_joins()
            if res:
                InterfazConsola.mostrar_tabla(*res)

        elif op == "5":
            print("1. Nuevo Material  2. Nuevo Punto")
            sub = input("> ")
            if sub == "1":
                db.material_crear(input("Nombre: "), input("Cat: "), "kg", 1)
            else:
                db.punto_crear(
                    input("Nombre: "), input("Muni: "), input("Dir: ")
                )

        elif op == "0":
            print("Saliendo...")
            break


if __name__ == "__main__":
    main()
