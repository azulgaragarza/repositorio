class Persona:
    def __init__(self):
        self._nombre="Nombre"
        self._dni="dni"
        self._edad="edad"
    def set_nombre(self, name): #funciones get y set no van ya que solo se pide una instancia en cada clase
        self._nombre = name     #y no que se le asigne valores
    def get_nombre(self):
        return self._nombre
    def set_edad(self,edad):
        self._edad=edad
    def get_edad(self):
        return self._edad
    def set_dni(self,dni):
        self._dni=dni
    def get_dni(self):
        return self._dni

class Estudiante(Persona):
    def __init__(self):
        self._curso=Curso()
    def agregar_estudiante(self):


class Curso():
    pass

    

una_persona=Persona()
una_persona.set_nombre("Azul")
una_persona.set_edad(19)
una_persona.set_dni(45805883)
print(una_persona.get_nombre())
print(una_persona.get_edad())
print(una_persona.get_dni())