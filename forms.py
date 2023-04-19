

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from pony.orm import db_session, select
from database import *

penitenciaria_choices = [
        ('emboscada', 'Penitenciaria Juana de la Vega'),
        ('pn_emboscada', 'Penitenciaria Nacional de Emboscada'),
        ('tacumbu', 'Penitenciaria Nacional de Tacumbù'), 
        ('buen_pastor', 'Penitenciaria Nacional del Buen Pastor'),
        ('la_esperanza', 'Penitenciaria La Esperanza'),
        ('regional_coronel_oviedo', 'Penitenciaria Regional de Coronel Oviedo'),
        ('regional_misiones', 'Penitenciaria Regional de Misiones'),
        ('pedro_juan', 'Penitenciaria Pedro Juan Caballero'),
        ('regional_de_concepcion', 'Penitenciaria Regional de Concepcion'),
        ('regional_de_san_pedro', 'Penitenciaria Regional de San Pedro'),
        ('juana_maria_de_lara', 'Penitenciaria Juana Ma. de Lara'),
        ('regional_cde', 'Penitenciaria Regional de Ciudad del Este'),
        ('regional_de_villarrica', 'Penitenciaria Regional de Villarrica'),
        ('regional_de_encarnacion', 'Penitenciaria Regional de Encarnacion')
    ]

class PersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()],
                         render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})
    apellido = StringField('Apellido', validators=[DataRequired()],
                        render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()],
                                 render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})
    genero = StringField('Género', validators=[DataRequired()],
                         render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})
    documento_identidad = StringField('Documento de Identidad', 
                                    validators=[DataRequired()],
                                    render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})
    penitenciaria = SelectField('Penitenciaria:', 
                                choices=penitenciaria_choices, 
                                validators=[DataRequired()],
                                description="",
                                option_widget={'class': 'px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none'})
    fecha_de_ingreso = DateField('Fecha de Ingreso', validators=[DataRequired()],
                                    render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})
    fecha_de_salida = DateField('Fecha de Salida', validators=[DataRequired()],
                                    render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})

    descripcion = TextAreaField('Descripción', validators=[DataRequired()],
                                render_kw={'class': "px-3 py-2 border border-accent rounded-md focus:border-2 focus:outline-none"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.penitenciaria.choices = penitenciaria_choices

class CreateReporteBuenaConductaForm(FlaskForm):
    id_persona_privada = StringField('ID Persona Privada de Libertad', validators=[DataRequired()])
    fecha_reporte = DateField('Fecha de Reporte', validators=[DataRequired()])
    conducta = StringField('Conducta', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[DataRequired()])

class UpdateReporteBuenaConductaForm(FlaskForm):
    fecha_reporte = DateField('Fecha de Reporte', validators=[DataRequired()])
    conducta = StringField('Conducta', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[DataRequired()])
        
class OTCForm(FlaskForm):
    id_persona_privada = StringField('ID Persona Privada de Libertad', validators=[DataRequired()])
    fecha_evaluacion = DateField('Fecha de Evaluación', format='%Y-%m-%d', validators=[DataRequired()])
    riesgo = StringField('Riesgo', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[DataRequired()])

class PlanSalidaForm(FlaskForm):

    id_persona_privada = StringField('ID Persona Privada de Libertad', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', format='%Y-%m-%d', validators=[DataRequired()])

    actividades = TextAreaField('Actividades', validators=[DataRequired()])
    seguimiento = TextAreaField('Seguimiento', validators=[DataRequired()])

class ReportePsicologicoForm(FlaskForm):
    id_persona_privada = StringField('ID Persona Privada', validators=[DataRequired()])
    fecha_evaluacion = DateField('Fecha de Evaluación', validators=[DataRequired()], format='%Y-%m-%d')
    diagnostico = TextAreaField('Diagnóstico', validators=[DataRequired()])
    recomendaciones = TextAreaField('Recomendaciones', validators=[DataRequired()])