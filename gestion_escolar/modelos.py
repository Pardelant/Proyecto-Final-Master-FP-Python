class Persona:
    # Atributo de clase (compartido por todas las instancias)
    total_vehiculos = 0

    def __init__(self, marca, nombre, email):
        """
        Método constructor (__init__):
        Se ejecuta automáticamente al crear un nuevo objeto Vehiculo.
        Define los atributos básicos del vehículo.
        """
        self._dni = marca
        self.nombre = nombre
        self.email = email

    def __str__(self):
        return print(f"{self.nombre} ({self._dni})")


class Asignatura:
    def __init__(self, nombre: str, nota: float = 0.0):
        self.nombre = nombre
        self.nota = nota
        self.set_nota(nota)

    def set_nota(self, valor: float):
        if 0 <= valor <= 10:
            self.nota = valor
        else:
            raise ValueError("La nota debe estar entre 0 y 10")

class Alumno(Persona):
    def __init__(self, dni: str, nombre: str, email: str):
        super().__init__(dni, nombre, email)
        self._asignaturas = []

    def matricular(self, asignatura: Asignatura):
        self._asignaturas.append(asignatura)

    def nota_media(self):
        if not self._asignaturas:
            return 0.0
        total = sum(a._nota for a in self._asignaturas)
        return total / len(self._asignaturas)

    def calificar(self, nombre_asignatura: str, nota: float):
        for asignatura in self._asignaturas:
            if asignatura._nombre == nombre_asignatura:
                asignatura.set_nota(nota)
                return
        raise ValueError("Asignatura no encontrada")