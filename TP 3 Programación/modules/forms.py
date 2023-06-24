from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Ingresar')

class RegisterForm(FlaskForm):
    name = StringField(label="Nombre", validators=[DataRequired()])
    apellido = StringField(label="Apellido", validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    claustro = SelectField(label='Claustro',validators=[DataRequired()],choices=[('estudiante','Estudiante'),('docente','Docente'),('PAyS','PAyS')]) #Cada tupla contiene dos elementos: el valor que se enviará al servidor cuando se seleccione la opción y la etiqueta que se mostrará en el formulario.
    password = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=8), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit = SubmitField(label='Registrar')