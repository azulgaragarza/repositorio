from flask_login import UserMixin,current_user
from server import db
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from flask import send_file

from modules.class_reclamo import Reclamo
from modules.class_departamento import Departamento
from modules.class_clasificador_reclamos import Clasificador_reclamos


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
            departamento_id = None
        else:
            departamento_id = departamento.id
        reclamo = Reclamo(
            id=None,
            usuario_creador=self.email,
            asunto=asunto,
            descripcion=descripcion,
            estado='Pendiente',
            adherente='',
            fecha=datetime.utcnow(),
            departamento_id=departamento_id
        )
        db.session.add(reclamo)
        db.session.commit()
    
    def adherirse_reclamo(self, reclamo_id):
        reclamo = db.session.get(Reclamo, reclamo_id)
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
    


class Jefe_departamento(Usuario):
    def crear_departamento(self,nombre,jefe):
        nombre.lower()
        departamento = Departamento.query.filter_by(nombre=nombre).first()
        if not departamento:
            departamento = Departamento(nombre=nombre,jefe=jefe)
            db.session.add(departamento)
            db.session.commit()
            return "Departamento creado"
        else:
            return "El departamento ya existe"
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
        
        reclamos_totales_2=reclamos_en_proceso+reclamos_resueltos
      
        if reclamos_en_proceso!=0:
            porcentaje_en_proceso = (reclamos_en_proceso*100)/reclamos_totales
        else:
            porcentaje_en_proceso = 0
        
        if reclamos_resueltos!=0:
            porcentaje_resueltos = (reclamos_resueltos*100)/reclamos_totales
        else:
            porcentaje_resueltos = 0

        if reclamos_totales == 0: #grafico vacio
            sizes = [1, 0]
            labels = ['', '']
            colors = ['gray', 'white']
            texto_abajo = "No hay reclamos"
        elif reclamos_resueltos==0 and reclamos_en_proceso==0:
            sizes = [1, 0]
            labels = ['', '']
            colors = ['gray', 'gray']
            texto_abajo = "No hay reclamos en proceso ni reclamos resueltos"
        elif reclamos_resueltos == 0 and reclamos_en_proceso != 0:
            sizes = [porcentaje_en_proceso, 0]
            labels = ['En proceso', 'Resueltos']
            colors = ['yellow', 'white']
            texto_abajo = ""
        elif reclamos_en_proceso == 0 and reclamos_resueltos != 0:
            sizes = [0, porcentaje_resueltos]
            labels = ['En proceso', 'Resueltos']
            colors = ['white', 'green']
            texto_abajo = ""
        else:
            sizes = [porcentaje_en_proceso, porcentaje_resueltos]
            labels = ['En proceso', 'Resueltos']
            colors = ['yellow', 'green']
            texto_abajo = ""

        plt.switch_backend('Agg')
        # Crear el diagrama circular
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.axis('equal')  # Para que el gráfico sea un círculo
        plt.text(0.5, -0.1, texto_abajo, ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
        plt.title(f'Total de reclamos: {reclamos_totales}, total de reclamos en proceso y resueltos: {reclamos_totales_2}')
        plt.suptitle('Estadísticas de reclamos')
        plt.savefig('static/grafico.png')

        #grafico palabras
        lista_reclamos = []
        for reclamo in reclamos:
            lista_reclamos.append(reclamo.descripcion)
        # Definir las palabras vacías (stop words)
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

        #frecuencia de las palabras clave
        if len(keywords) == 0:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate("None")
        else:
            fdist = FreqDist(keywords)
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(fdist)

        # Mostrar el gráfico de Word Cloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.suptitle('Palabras claves en los reclamos')
        plt.savefig('static/grafico_palabras_claves.png')
        plt.switch_backend('TkAgg')
    
    def cambiar_estado(self,reclamo_id,estado):
        reclamo = Reclamo.query.filter_by(id=reclamo_id).first()
        reclamo.estado = estado
        db.session.commit()

    def derivar_reclamo(self,reclamo_id,departamento):
        reclamo = Reclamo.query.filter_by(id=reclamo_id).first()
        if departamento is not None:
            reclamo.departamento_id = int(departamento)
        db.session.commit()

