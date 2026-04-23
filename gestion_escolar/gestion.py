class centro_educativo:
    def __init__(self):
        self._usuarios = []

    def agregar_usuario(self, persona):
        self._usuarios.append(persona)

    def listar_usuarios(self):
        for usuario in self._usuarios:
            print(usuario)

    def obtener_usuarios(self):
        return list(self._usuarios)
