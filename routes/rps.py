from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, UserMixin, login_required
from forms import ReportePsicologicoForm
from database import *

routingPS = Blueprint('ps', __name__, template_folder='templates')


@routingPS.route('/insertar_reporte', methods=['GET', 'POST'])
def insertar_reporte_psicologico():
    form = ReportePsicologicoForm()
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

@routingPS.route('/modificar_reporte/<int:id>', methods=['GET', 'POST']) #Defino una ruta que reciba el identificador del registro a modificar y muestre un formulario con los datos actuales del registro.
@db_session()
def modificar_reporte(id):
    # Obtener el registro a modificar de la base de datos
    reporte = ReportePsicologico.get(id_reporte_psicologico=id)

    # Si el registro no existe, mostrar un error
    if not reporte:
        return 'Registro no encontrado', 404

    #Crear el formulario de modificación
    form = ReportePsicologicoForm(obj=reporte)

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

@routingPS.route('/eliminar_reporte/<int:id>', methods=['GET', 'POST']) #Defino una ruta que reciba el identificador del registro a modificar y muestre un formulario con los datos actuales del registro.
@db_session()
def eliminar_reporte(id):
    # Obtener el registro a modificar de la base de datos
    reporte = ReportePsicologico.get(id_reporte_psicologico=id)

    # Si el registro no existe, mostrar un error
    if not reporte:
        return 'Registro no encontrado', 404

    #Crear el formulario de modificación
    form = ReportePsicologicoForm(obj=reporte)

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