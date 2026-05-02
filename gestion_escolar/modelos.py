from abc import ABC, abstractmethod


class Persona(ABC):
    def __init__(self, dni, nombre, email):
        self._dni = dni
        self.nombre = nombre
        self.email = email

    @abstractmethod
    def __str__(self):
        pass


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

    def to_dict(self):
        return {"nombre": self.nombre, "nota": self.nota}


class Alumno(Persona):
    def __init__(self, dni: str, nombre: str, email: str):
        super().__init__(dni, nombre, email)
        self._asignaturas = []

    def matricular(self, asignatura: Asignatura):
        self._asignaturas.append(asignatura)

    def nota_media(self):
        if not self._asignaturas:
            return 0.0
        total = sum(asignatura.nota for asignatura in self._asignaturas)
        return total / len(self._asignaturas)

    def calificar(self, nombre_asignatura: str, nota: float):
        for asignatura in self._asignaturas:
            if asignatura.nombre == nombre_asignatura:
                asignatura.set_nota(nota)
                return
        raise ValueError("Asignatura no encontrada")

    def to_dict(self):
        """Lógica para exportar a JSON"""
        return {
            "dni": self._dni,
            "nombre": self.nombre,
            "email": self.email,
            "asignaturas": [asig.to_dict() for asig in self._asignaturas],
        }

    def __str__(self):
        return f"Alumno: {self.nombre} ({self._dni})"


class Profesor(Persona):
    def __init__(self, dni: str, nombre: str, email: str, especialidad: str):
        super().__init__(dni, nombre, email)
        self.especialidad = especialidad

    def to_dict(self):
        return {
            "dni": self._dni,
            "nombre": self.nombre,
            "email": self.email,
            "especialidad": self.especialidad,
            "asignaturas_impartidas": self.asignaturas_impartidas,
        }

    def __str__(self):
        return f"Profesor: {self.nombre} ({self._dni}) - {self.especialidad}"
