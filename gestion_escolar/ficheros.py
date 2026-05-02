import json


class ficheros:
    
    def leerJSON():
        contenidojson = open("alumnos.json", "r")
        return contenidojson.read()

    def escribirJSON():

        pass
