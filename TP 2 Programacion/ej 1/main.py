class Persona:
    def __init__(self,nom,dni):
        self.nombre=nom
        self.dni=dni
        #self.edad=edad    
    def get_nombre(self):
        return self.nombre
    #def get_edad(self):
        return self.edad
    def get_dni(self):
        return self.dni


class Estudiante(Persona):
    def __init__(self, nom, dni):
        super().__init__(nom, dni)
        self.legajo="legajo"
        #self.curso=Curso()
        
    def obtener_informacion(self):
        return f"Nombre: {self.nombre}, DNI: {self.dni}"    



class Curso():
    def __init__(self, nombre_curso, carga_horaria):
        self.nombre_curso= nombre_curso
        self.carga_horaria= carga_horaria
        self.cursos=[]
    
    def listar_curso(self, curso):
        self.cursos.append(curso)
    
    def asignar_profesor(self,profesor):
        if self in self.cursos:
            self.profesor_curso=profesor.nombre_profesor
        pass

    def devolver_curso(self):
        if self in self.cursos:
            print("Nombre del curso:", self.nombre_curso)
            print("Carga horaria:", self.carga_horaria)
            print("Profesor:", self.profesor_curso)
    

class Facultad():
    def __init__(self, nombre):
        if isinstance(nombre, str):
            self.nombre_facultad = nombre
        else:
            raise ValueError("El nombre de la facultad está mal ingresado")
        self.estudiantes = []
        self.departamentos = []

    def agregar_estudiantes(self, estudiante):
        self.estudiantes.append(estudiante)
        
    def devolver_estudiantes(self):
        print(f"Estudiantes en la {self.nombre_facultad}:")
        for estudiante in self.estudiantes:
            print(estudiante.obtener_informacion())
    
    def crear_departamento(self,departamento):
        self.departamentos.append(departamento)

class Profesor(Persona):
    def __init__(self, nom, dni):
        super().__init__(nom, dni)
        self.nombre_profesor=nom
        self.dni_profesor=dni

class Departamento():
    def __init__(self,nombre):
        self.nombre_departamento=nombre
        self.profesores=[]

    def agregar_profesores(self,profesor):
        self.profesores.append(profesor)

    def devolver_profesores(self):
        print(f"Profesores en el departamento de {self.nombre_departamento}:")
        for profe in self.profesores:
            print(f"Nombre: {profe.nombre_profesor}, DNI: {profe.dni_profesor}")

    def asignar_director(self,profesor):
        if profesor in self.profesores:
            self.director=profesor
            self.nombre_director=profesor.nombre_profesor
        return print(f"El director de {self.nombre_departamento} es {self.nombre_director}")



# Instancias de la clase Persona
persona1= Persona("Naza", 45552845)
print(persona1.get_dni())

# Instancias de la clase Estudiante
estudiante1 = Estudiante("Sol", 44442844)
estudiante2 = Estudiante("Cielo", 44342844)
estudiante3 = Estudiante("Nube", 45442844)

# Instancias de la clase Profesor
profesor1=Profesor("Hugo",25806994)
profesor2=Profesor("Graciela", 26705664)
profesor3=Profesor("Liliana", 28490568)
profesor4=Profesor("Gabriela", 26345678)

# Instancias de la clase Facultad 
facultad = Facultad("UNER")

facultad.agregar_estudiantes(estudiante1)
facultad.agregar_estudiantes(estudiante2)
facultad.agregar_estudiantes(estudiante3)

facultad.devolver_estudiantes()
print()

# Instancias de la clase Curso
curso1 = Curso("Matemáticas", 60)
curso2 = Curso("Inglés", 45)

curso1.listar_curso(curso1)
curso2.listar_curso(curso2)

curso1.asignar_profesor(profesor3)
curso2.asignar_profesor(profesor4)

curso1.devolver_curso()
curso2.devolver_curso()
print()


# Instancias de la clase Departamento
departamento1=Departamento("Fisica")
departamento1.agregar_profesores(profesor1)
departamento1.agregar_profesores(profesor2)

departamento1.devolver_profesores()
print()
departamento1.asignar_director(profesor2)
