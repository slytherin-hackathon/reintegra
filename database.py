from flask import Flask
from flask_login import UserMixin
from pony.orm import *
from datetime import date

app = Flask(__name__)

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
    fotografia = Optional(str)
    organismo_tecnico_criminologico = Set('OrganismoTecnicoCriminologico') # Define reverse attribute
    plan_salida_libertad = Set('PlanSalidaLibertad') # Define reverse attribute
    reporte_psicologico = Set('ReportePsicologico') # Define reverse attribute
    reporte_buena_conducta = Set('ReporteBuenaConducta') # Define reverse attribute
    

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

# Define UserLogin entity
class UserLogin(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    password = Required(str)

# Generate database tables
db.generate_mapping(create_tables=True)
