class Persona:
    def __init__(self,nom,dni):
        self._nombre=nom
        self._dni=dni
        self._edad="edad"
    #def set_nombre(self, name): 
        #self._nombre = name     
    def get_nombre(self):
        return self._nombre
    #def set_edad(self,edad):
        #self._edad=edad
    def get_edad(self):
        return self._edad
    #def set_dni(self,dni):
        #self._dni=dni
    def get_dni(self):
        return self._dni

class Estudiante(Persona):
    def __init__(self,nom,dni):
        estudiantes= {
                "nombre":nom,
                "dni":dni
        }
        self._legajo="legajo"
        self._curso=Curso()
        super().__init__(nom,dni)
    def agregar_estudiante(self):
        pass
    #def 


class Curso():
    def __init__(self):
        self._nombre_curso="Nombre del curso"
        #self._estudiante=Estudiante()
        self._carga_horaria="Carga horaria"
    
    
class Profesor(Persona):
    def __init__(self):

        super().__init__()
        pass

class Facultad():
    def __init__(self):
        self._nombre_facultad="Nombre de la facultad"
    def agregar_estudiante(self, nom, dni, estudiantes):
        nuevo_estudiante = Estudiante(nom, dni)
        if dni not in estudiantes:
            estudiantes[dni] = dni
            estudiantes[nom]= nom
        else:
            raise Exception("Ya esta inscripto en la facultad")
    def devolver_estudiante(self, nom, estudiantes):
        return estudiantes[nom]

class Departamento():
    def __init__(self):
        pass

una_persona=Persona("Naza",45552845)
#un_estudiante=Estudiante("Naza",45552845) #instancias de las clases (objetos)
#un_profesor=Profesor()
UNER=Facultad()
UNER.agregar_estudiante("Azul",45805883, estudiantes)
print(UNER.devolver_estudiante("Azul"))
#una_persona.set_nombre("Azul")
#una_persona.set_edad(19) 
#una_persona.set_dni(45805883)
#print(una_persona.get_nombre())
#print(una_persona.get_edad())
#print(una_persona.get_dni())