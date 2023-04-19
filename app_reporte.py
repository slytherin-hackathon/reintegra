from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, UserMixin, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired
from pony.orm import *
from datetime import date

app = Flask(__name__)
app.secret_key = 'millavesecreta'

# Set up SQLite database connection
db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class ReportePsicologico(db.Entity):
    id_reporte_psicologico = PrimaryKey(int, auto=True)
    id_persona_privada = Required(int)
    fecha_evaluacion = Required(date)
    diagnostico = Required(LongStr)
    recomendaciones = Required(LongStr)


class ReporteForm(FlaskForm):
    id_persona_privada = StringField('ID Persona Privada', validators=[DataRequired()])
    fecha_evaluacion = DateField('Fecha de Evaluación', validators=[DataRequired()], format='%Y-%m-%d')
    diagnostico = TextAreaField('Diagnóstico', validators=[DataRequired()])
    recomendaciones = TextAreaField('Recomendaciones', validators=[DataRequired()])

# Generate database tables
db.generate_mapping(create_tables=True)

@app.route('/insertar_reporte', methods=['GET', 'POST'])
def insertar_reporte_psicologico():
    form = ReporteForm()
    if request.method == 'POST':
        id_persona_privada = form.id_persona_privada.data
        fecha_evaluacion = form.fecha_evaluacion.data
        diagnostico = form.diagnostico.data
        recomendaciones = form.recomendaciones.data
        with db_session:
            reporte_psicologico = ReportePsicologico(id_persona_privada=id_persona_privada,
                                                     fecha_evaluacion=fecha_evaluacion,
                                                     diagnostico=diagnostico,
                                                     recomendaciones=recomendaciones)
        if reporte_psicologico:
            return jsonify({'message': 'Reporte psicológico agregado exitosamente'})
            #return "Usuario registrado con èxito"
        else:
            return jsonify({'message': 'error'})
            #return render_template('insert_reporte.html')
    return render_template('insert_reporte.html', form=form)

@app.route('/modificar_reporte/<int:id>', methods=['GET', 'POST']) #Defino una ruta que reciba el identificador del registro a modificar y muestre un formulario con los datos actuales del registro.
@db_session()
def modificar_reporte(id):
    # Obtener el registro a modificar de la base de datos
    reporte = ReportePsicologico.get(id_reporte_psicologico=id)

    # Si el registro no existe, mostrar un error
    if not reporte:
        return 'Registro no encontrado', 404

    #Crear el formulario de modificación
    form = ReporteForm(obj=reporte)

    #Renderizar la plantilla con el reporte
    #return render_template('ver_reporte.html', reporte=reporte)

    # Procesar la solicitud de modificación
    if request.method == 'POST':
        # Actualizar los datos del registro
        reporte.id_persona_privada = form.id_persona_privada.data
        reporte.fecha_evaluacion = form.fecha_evaluacion.data
        reporte.diagnostico = form.diagnostico.data
        reporte.recomendaciones = form.recomendaciones.data

        # Guardar los cambios en la base de datos
        commit()

        # Redirigir al usuario a la página de detalles del registro
        #return redirect(url_for('ver_reporte', id=id_reporte_psicologico))

    # Mostrar el formulario de modificación
    return render_template('modificar_reporte.html', form=form, id=id)

@app.route('/eliminar_reporte/<int:id>', methods=['GET', 'POST']) #Defino una ruta que reciba el identificador del registro a modificar y muestre un formulario con los datos actuales del registro.
@db_session()
def eliminar_reporte(id):
    # Obtener el registro a modificar de la base de datos
    reporte = ReportePsicologico.get(id_reporte_psicologico=id)

    # Si el registro no existe, mostrar un error
    if not reporte:
        return 'Registro no encontrado', 404

    #Crear el formulario de modificación
    form = ReporteForm(obj=reporte)

    #Renderizar la plantilla con el reporte
    #return render_template('ver_reporte.html', reporte=reporte)

    # Procesar la solicitud de eliminar
    if request.method == 'POST':
       # ELiminar los datos del registro
        reporte.delete()

        # Guardar los cambios en la base de datos
        commit()

        # Redirigir al usuario a la página de detalles del registro
        #return redirect(url_for('ver_reporte', id=id_reporte_psicologico))

    # Mostrar el formulario de modificación
    return render_template('eliminar_reporte.html', form=form, id=id)



if __name__ == '__main__':
    app.run(debug=True)
