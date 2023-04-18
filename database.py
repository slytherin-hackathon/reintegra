from flask import Flask
from flask_login import UserMixin
from pony.orm import *
from datetime import date

db = Database()
# Set up SQLite database connection
db = Database()

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

# Define models using Pony ORM entities
class PersonaPrivadaDeLibertad(db.Entity):
    id_persona_privada = PrimaryKey(int, auto=True)
    nombre = Required(str)
    apellido = Required(str)
    fecha_nacimiento = Required(date)
    genero = Required(str)
    documento_identidad = Required(str)
    # fotografia = Required(str)
    organismo_tecnico_criminologico = Set('OrganismoTecnicoCriminologico') # Define reverse attribute
    plan_salida_libertad = Set('PlanSalidaLibertad') # Define reverse attribute
    reporte_psicologico = Set('ReportePsicologico') # Define reverse attribute
    reporte_buena_conducta = Set('ReporteBuenaConducta') # Define reverse attribute
    
    def __str__(self):
        return str(self.id_persona_privada)

class OrganismoTecnicoCriminologico(db.Entity):
    id_otc = PrimaryKey(int, auto=True)
    id_persona_privada = Required(PersonaPrivadaDeLibertad) # Update reference to entity
    fecha_evaluacion = Required(date)
    riesgo = Required(str)
    observaciones = Required(LongStr)

class PlanSalidaLibertad(db.Entity):
    id_plan_salida = PrimaryKey(int, auto=True)
    id_persona_privada = Required(PersonaPrivadaDeLibertad) # Update reference to entity
    fecha_inicio = Required(date)
    fecha_fin = Required(date)
    actividades = Required(LongStr)
    seguimiento = Required(LongStr)

class ReportePsicologico(db.Entity):
    id_reporte_psicologico = PrimaryKey(int, auto=True)
    id_persona_privada = Required(PersonaPrivadaDeLibertad) # Update reference to entity
    fecha_evaluacion = Required(date)
    diagnostico = Required(LongStr)
    recomendaciones = Required(LongStr)

class ReporteBuenaConducta(db.Entity):
    id_reporte_buena_conducta = PrimaryKey(int, auto=True)
    id_persona_privada = Required(PersonaPrivadaDeLibertad) # Update reference to entity
    fecha_reporte = Required(date)
    conducta = Required(str)
    observaciones = Required(LongStr)

class User(db.Entity, UserMixin):
    username = Required(str, unique=True)
    email = Required(str)
    password = Required(str)

class Image(db.Entity):
    id_image = PrimaryKey(int, auto=True)
    filename = Required(str)
    image = Required(LongStr)
    # persona_privada_de_libertad = Optional(PersonaPrivadaDeLibertad) # Update reference to entity
    
# Generate database tables
db.generate_mapping(create_tables=True)  # This will create tables for registered models
