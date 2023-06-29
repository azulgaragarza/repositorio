from flask_login import UserMixin
from server import db
from datetime import datetime
from flask_login import current_user
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    apellido = db.Column(db.String(1000))
    claustro = db.Column(db.String(100))

    def __init__(self, email, password, name, apellido,claustro):
        self.email = email
        self.password = password
        self.name = name
        self.apellido = apellido
        self.claustro = claustro


class Usuario_final(Usuario):
    def crear_reclamo(self, asunto, descripcion):
        departamento = Clasificador_reclamos.clasificar_reclamo(asunto, descripcion)
        if departamento is None:
            departamento = "Esperando asignacion de departamento"
        reclamo = Reclamo(
        id = None,
        usuario_creador=self.email,
        asunto=asunto,
        descripcion=descripcion,
        departamento=departamento,
        estado='En proceso',
        adherente='',
        fecha=datetime.utcnow(),
        departamento_id=departamento.id
        )
        db.session.add(reclamo)
        db.session.commit()
    
    def adherirse_reclamo(self, reclamo_id):
        reclamo = Reclamo.query.get(reclamo_id)
        if reclamo:
            if reclamo.usuario_creador == current_user.email:
                return "No se puede"
            else:
                if reclamo.adherente == '':
                    reclamo.adherente = current_user.email
                else:
                    if current_user.email not in reclamo.adherente:
                        reclamo.adherente = reclamo.adherente + f', { current_user.email}'
                    else:
                        return False
            db.session.commit()
            return True
        else:
            return False
    

class Reclamo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    usuario_creador = db.Column(db.String(100))
    asunto = db.Column(db.String(1000))
    descripcion = db.Column(db.String(1000))
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))
    departamento = db.relationship('Departamento', backref=db.backref('reclamos'))
    estado =  db.Column(db.String(100))
    adherente = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    #imagen = db.Column(db.LargeBinary)
    
    def __init__(self, id, asunto, descripcion, fecha, usuario_creador, departamento, departamento_id, estado, adherente):
        self.id = id
        self.asunto = asunto
        self.descripcion = descripcion
        self.fecha = fecha
        self.usuario_creador = usuario_creador
        self.departamento = departamento
        self.departamento_id = departamento_id
        self.estado = estado
        self.adherente = adherente

class Jefe_departamento(Usuario):
    def crear_departamento(self,nombre,jefe):
        departamento = Departamento.query.filter_by(nombre=nombre).first()
        if not departamento:
            departamento = Departamento(nombre=nombre,jefe=jefe)
            db.session.add(departamento)
            db.session.commit()
    def generar_graficos(self):
        reclamos_totales = 0
        reclamos_en_proceso = 0
        reclamos_resueltos  = 0
        departamento = Departamento.query.filter_by(id=current_user.id).first()
        reclamos = Reclamo.query.filter_by(departamento_id=departamento.id).all()
        for reclamo in reclamos:
            reclamos_totales=reclamos_totales + 1
            if reclamo.estado == "En proceso":
                reclamos_en_proceso = reclamos_en_proceso + 1
            elif reclamo.estado == "Resuelto":
                reclamos_resueltos = reclamos_resueltos + 1
        if reclamos_en_proceso!=0:
            porcentaje_en_proceso = (reclamos_en_proceso*100)/reclamos_totales
        else:
            porcentaje_en_proceso = 0
        
        if reclamos_resueltos!=0:
            porcentaje_resueltos = (reclamos_resueltos*100)/reclamos_totales
        else:
            porcentaje_resueltos = 0

        if reclamos_totales == 0:  
            sizes = [0, 1]  
        else:
            sizes = [porcentaje_en_proceso, porcentaje_resueltos]
        
        labels = ['En proceso', 'Resueltos']
        colors = ['yellow', 'green']

        plt.switch_backend('Agg')
        # Crear el diagrama circular
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.axis('equal')  # Para que el gráfico sea un círculo

        plt.title(f'Total de reclamos: {reclamos_totales}')
        plt.suptitle('Estadísticas de reclamos')
        plt.savefig('static\\grafico.png')

        #Obtener palabras clave
        
        # Descargar los recursos necesarios de NLTK (solo se requiere hacer una vez)
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Obtener los reclamos (supongamos que los tienes en una lista llamada 'reclamos')
        lista_reclamos = []
        for reclamo in reclamos:
            lista_reclamos.append(reclamo.descripcion)

        # Definir las palabras vacías (stop words) que deseas filtrar
        stop_words = set(stopwords.words('spanish'))

        # Procesar cada reclamo y extraer las palabras clave

        keywords = []
        for reclamo in lista_reclamos:
            # Tokenizar el reclamo en palabras individuales
            tokens = word_tokenize(reclamo.lower())
            # Filtrar las palabras vacías
            filtered_words = [word for word in tokens if word.isalnum() and word not in stop_words]
            # Agregar las palabras clave a la lista
            keywords.extend(filtered_words)

        # Calcular la frecuencia de las palabras clave
        if len(keywords) == 0:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate("None")
        else:
            fdist = FreqDist(keywords)
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(fdist)

        # Mostrar el gráfico de Word Cloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.suptitle('Nube de palabras de los reclamos')
        plt.savefig('static\\grafico_palabras_claves.png')
        plt.switch_backend('TkAgg')
    
    def cambiar_estado(self,reclamo_id,estado):
        reclamo = Reclamo.query.filter_by(id=reclamo_id).first()
        reclamo.estado = estado
        db.session.commit()


class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    jefe = db.Column(db.String(200))

    def __init__(self, nombre, jefe):
        self.nombre = nombre
        self.jefe = jefe
        
    def cambiar_jefe(self,jefe_nuevo,id_depto):
        departamento = Departamento.query.filter_by(id=id_depto).first()
        departamento.jefe = jefe_nuevo
        db.session.commit()

class Secretario_tecnico(Usuario):
    pass


class Clasificador_reclamos():
    @staticmethod
    def clasificar_reclamo(asunt, description):
        palabras_clave_dpto1 = ['plan de estudio','currículo académico','programas académicos','carrera','horarios','aulas','calificación','calificaciones','catedra','profesor','examen','asignaturas','pasantías','materia']
        palabras_clave_dpto2 = ['campus','correo electrónico institucional','software institucional','gestión académica',' aula virtual','conexion','wifi']
        palabras_clave_dpto3 = ['beca', 'salud', 'residencia', 'transporte','inscripcion','bienestar estudiantil','atención médica','Actividades extracurriculares']

        asunto = asunt.lower()
        descripcion = description.lower()

        for palabra in palabras_clave_dpto1:
            if palabra in asunto or palabra in descripcion:
                return Departamento.query.filter_by(id=1).first()

        for palabra in palabras_clave_dpto2:
            if palabra in asunto or palabra in descripcion:
                return Departamento.query.filter_by(id=2).first()
    
        for palabra in palabras_clave_dpto3:
            if palabra in asunto or palabra in descripcion:
                return Departamento.query.filter_by(id=3).first()
        
        # Si no se cumple ninguna regla, clasificar en un departamento por defecto
        return None