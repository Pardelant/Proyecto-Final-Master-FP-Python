import json
import os


class GestorFicheros:
    # ATRIBUTOS DE CLASE (Compartidos por todas las instancias)
    ficheros_abiertos = 0
    operaciones_ficheros = 0

    def __init__(self, ruta: str):
        """ 
        Inicialización para un fichero concreto.
        """
        self._ruta = ruta
        GestorFicheros.ficheros_abiertos += 1

    def leer_json(self) -> list:
        """
        Lectura de ficheros JSON (no formatea, devuelve lista de diccionarios)
        """
        GestorFicheros.operaciones_ficheros += 1
        
        if not os.path.exists(self._ruta):
            return []
            
        try:
            with open(self._ruta, "r", encoding="utf-8") as f:
                contenido = json.load(f)
                return contenido if contenido else []
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error al leer el fichero {self._ruta}: {e}")
            return []

    def guardar_json(self, contenido: list) -> None:
        """
        Escritura de ficheros json
        """
        GestorFicheros.operaciones_ficheros += 1
        
        try:
            with open(self._ruta, "w", encoding="utf-8") as f:
                json.dump(contenido, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar en el fichero {self._ruta}: {e}")