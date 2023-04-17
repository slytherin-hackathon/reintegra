from flask import Flask
from pony.orm import *

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

class OrganismoTecnicoCriminologico(db.Entity):
    id_otc = PrimaryKey(int, auto=True)
    id_persona_privada = ForeignKey(PersonaPrivadaDeLibertad)
    fecha_evaluacion = Required(date)
    riesgo = Required(str)
    observaciones = Required(LongStr)

class PlanSalidaLibertad(db.Entity):
    id_plan_salida = PrimaryKey(int, auto=True)
    id_persona_privada = ForeignKey(PersonaPrivadaDeLibertad)
    fecha_inicio = Required(date)
    fecha_fin = Required(date)
    actividades = Required(LongStr)
    seguimiento = Required(LongStr)

class ReportePsicologico(db.Entity):
    id_reporte_psicologico = PrimaryKey(int, auto=True)
    id_persona_privada = ForeignKey(PersonaPrivadaDeLibertad)
    fecha_evaluacion = Required(date)
    diagnostico = Required(LongStr)
    recomendaciones = Required(LongStr)

class ReporteBuenaConducta(db.Entity):
    id_reporte_buena_conducta = PrimaryKey(int, auto=True)
    id_persona_privada = ForeignKey(PersonaPrivadaDeLibertad)
    fecha_reporte = Required(date)
    conducta = Required(str)
    observaciones = Required(LongStr)

# Generate database tables
db.generate_mapping(create_tables=True)
