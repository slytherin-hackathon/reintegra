from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired
from pony.orm import db_session, select
from pony.orm.core import EntityMeta
from database import Image, db

# Create Flask-WTF form for PersonaPrivadaDeLibertad
class PersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    genero = StringField('Género', validators=[DataRequired()])
    documento_identidad = StringField('Documento de Identidad', validators=[DataRequired()])
    # fotografia = FileField('Fotografía', validators=[
    #     FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG and PNG images are allowed!')
    # ])

    # Optional: If you want to customize the filename when saving the file
    def save_fotografia(self, folder):
        if self.fotografia.data:
            filename = secure_filename(self.fotografia.data.filename)
            self.fotografia.data.save(f'{folder}/{filename}')
            # create register of image in db
            with db_session:
                filename = Image(filename=filename)
            return filename
        


# Create Flask-WTF form for Organismo Tecnico Criminologico
class OTCForm(FlaskForm):
    id_persona_privada = StringField('ID Persona Privada de Libertad', validators=[DataRequired()])
    fecha_evaluacion = DateField('Fecha de Evaluación', format='%Y-%m-%d', validators=[DataRequired()])
    riesgo = StringField('Riesgo', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[DataRequired()])

