class DatoInvalido(Exception):
    print("dato invalido")


class Duplicado(Exception):
    print("duplicado")


class Validator:
    @staticmethod
    def validar_dni(texto: str) -> bool:
        if not isinstance(texto, str):
            return False

        texto = texto.strip()
        if len(texto) != 9:
            return False

        numeros = texto[:8]
        letra = texto[8]

        if not numeros.isdigit() or not letra.isalpha():
            return False

        return True

    @staticmethod
    def formatear_nombre(texto: str) -> str:
        if texto is None:
            raise DatoInvalido()

        texto = str(texto).strip()
        if not texto:
            raise DatoInvalido()

        return texto.capitalize()
