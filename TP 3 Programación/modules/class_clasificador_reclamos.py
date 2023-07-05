from modules.class_departamento import Departamento


class Clasificador_reclamos():
    @staticmethod
    def clasificar_reclamo(asunt, description):
        palabras_clave_dpto1 = ['plan de estudio','currículo académico','programas académicos','carrera','horarios','aula','calificación','calificaciones','catedra','profesor','examen','asignaturas','pasantías','materia', 'parcial', 'final']
        palabras_clave_dpto2 = ['campus','correo electrónico institucional','software institucional','gestión académica',' aula virtual','conexion','wifi']
        palabras_clave_dpto3 = ['beca', 'salud', 'residencia', 'transporte','inscripcion','bienestar estudiantil','atención médica','actividades extracurriculares', 'comedor', 'comida']
        asunto = asunt.lower()
        descripcion = description.lower()

        try:
            for palabra in palabras_clave_dpto1:
                if palabra in asunto or palabra in descripcion:
                    return Departamento.query.filter_by(id=1).first()

            for palabra in palabras_clave_dpto2:
                if palabra in asunto or palabra in descripcion:
                    return Departamento.query.filter_by(id=2).first()
        
            for palabra in palabras_clave_dpto3:
                if palabra in asunto or palabra in descripcion:
                    return Departamento.query.filter_by(id=3).first()
        except Exception as e:
            print("Error al clasificar reclamo:", e)
        return None