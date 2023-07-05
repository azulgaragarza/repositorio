class Persona:
    def __init__(self,nom,dni):
        self.nombre=nom
        self.dni=dni
    def get_nombre(self):
        return self.nombre
    def get_dni(self):
        return self.dni


class Estudiante(Persona):
    def __init__(self, nom, dni):
        super().__init__(nom, dni)
        self.legajo="legajo"
        self.cursos_inscriptos=[]
        
    def obtener_informacion(self):
        return f"Nombre: {self.nombre}, DNI: {self.dni}"  

    def inscribirse_curso(self,curso):
        self.cursos_inscriptos.append(curso)

class Curso():
    def __init__(self, nombre_curso, carga_horaria):
        self.nombre_curso= nombre_curso
        self.carga_horaria= carga_horaria
        self.alumnos=[]
        self.profesor_curso = ""
    
    def inscribir_alumno(self,alumno):
        self.alumnos.append(alumno) 

    def asignar_profesor(self,profesor):
        self.profesor_curso=profesor

    def devolver_curso(self):
        print("Nombre del curso:", self.nombre_curso)
        print("Carga horaria:", self.carga_horaria)
        print("Profesor:", self.profesor_curso)
        print("Alumnos inscriptos:")
        for alumno in self.alumnos:
            print(f"{alumno.nombre}, Dni: {alumno.dni}")


class Facultad():
    def __init__(self, nombre,nombre_depto):
        if isinstance(nombre, str):
            self.nombre_facultad = nombre
        else:
            raise ValueError("El nombre de la facultad está mal ingresado")
        self.estudiantes = []
        self.departamentos = {nombre_depto:Departamento(nombre_depto)}

    def agregar_estudiantes(self, estudiante):
        self.estudiantes.append(estudiante)
        
    def devolver_estudiantes(self):
        print(f"Estudiantes en la {self.nombre_facultad}:")
        for estudiante in self.estudiantes:
            print(estudiante.obtener_informacion())
    
    def crear_departamento(self,nombre_depto):
        self.departamentos[nombre_depto]=Departamento(nombre_depto)

    def asignar_profesor_depto(self,profesor,nombre_depto):
        self.departamentos[nombre_depto].agregar_profesor(profesor)
        profesor.asignar_departamento(self.departamentos[nombre_depto])

    def asignar_director_depto(self,profesor,nombre_depto):
        self.departamentos[nombre_depto].asignar_director(profesor)

    def asignar_estudiante_curso(self,estudiante,curso):
        curso.inscribir_alumno(estudiante)
        estudiante.inscribirse_curso(curso)

    def asignar_profesor_curso(self,profesor,curso):
        curso.asignar_profesor(profesor)
        profesor.asignar_curso(curso)


class Profesor(Persona):
    def __init__(self, nom, dni):
        super().__init__(nom, dni)
        self.cursos=[]
        self.departamentos=[]
    
    def asignar_departamento(self,departamento):
        self.departamentos.append(departamento.nombre_departamento)

    def asignar_curso(self,curso):
        self.cursos.append(curso)

class Departamento():
    def __init__(self,nombre):
        self.nombre_departamento=nombre
        self.profesores=[]

    def agregar_profesor(self,profesor):
        self.profesores.append(profesor)

    def devolver_profesores(self):
        print(f"Profesores en el departamento de {self.nombre_departamento}:")
        for profe in self.profesores:
            print(f"Nombre: {profe.nombre}, DNI: {profe.dni}")

    def asignar_director(self,profesor):
        if profesor in self.profesores:
            self.director=profesor
            self.nombre_director=profesor.nombre
        

# Instancias de la clase Persona
persona1= Persona("Azul", 45552845)
print(f'El DNI de {persona1.nombre} es {persona1.get_dni()}')

# Instancias de la clase Estudiante
estudiante1 = Estudiante("Sol", 44442844)
estudiante2 = Estudiante("Cielo", 44342844)
estudiante3 = Estudiante("Nube", 45442844)

# Instancias de la clase Profesor
profesor1=Profesor("Hugo",25806994)
profesor2=Profesor("Graciela", 26705664)
profesor3=Profesor("Liliana", 28490568)
profesor4=Profesor("Gabriela", 26345678)

# Instancias de la clase Curso
curso1 = Curso("Matemáticas", 60)
curso2 = Curso("Inglés", 45)

# Instancias de la clase Facultad 
facultad = Facultad("UNER","Fisica") #crea la facultad, junto con un departamento

facultad.agregar_estudiantes(estudiante1)
facultad.agregar_estudiantes(estudiante2)
facultad.agregar_estudiantes(estudiante3)
facultad.devolver_estudiantes()
print()

#asignar profesores y directores desde la facultad
facultad.asignar_profesor_depto(profesor1,"Fisica")
print(f'los departamentos de {profesor1.nombre} son: {profesor1.departamentos}')
facultad.asignar_profesor_depto(profesor2,"Fisica")
print(f'los departamentos de {profesor2.nombre} son: {profesor2.departamentos}')
facultad.asignar_director_depto(profesor2,"Fisica") 
print(f'El director del departamento de Fisica es {facultad.departamentos["Fisica"].director.nombre}')
print()

facultad.asignar_estudiante_curso(estudiante1,curso1)
facultad.asignar_estudiante_curso(estudiante2,curso1)
curso1.devolver_curso()

facultad.asignar_profesor_curso(profesor3,curso2)
print(f'{profesor3.nombre} enseña en:')
for curso in profesor3.cursos:
    print(curso.nombre_curso)

