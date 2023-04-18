from flask import Blueprint, render_template, request, redirect, url_for
from database import * 
from forms import OTCForm

routingOTC = Blueprint('otc', __name__)

# CRUD operations

@routingOTC.route('/')
def index():
    otc_list = OrganismoTecnicoCriminologico.select()
    return render_template('otc/index.html', otc_list=otc_list)

@routingOTC.route('/create', methods=['GET', 'POST'])
def create():
    form = OTCForm()
    if form.validate_on_submit():
        with db_session:
            persona = PersonaPrivadaDeLibertad[form.id_persona_privada.data]
            print({'persona': persona})
            otc = OrganismoTecnicoCriminologico(
                id_persona_privada=persona.id_persona_privada,
                fecha_evaluacion=form.fecha_evaluacion.data,
                riesgo=form.riesgo.data,
                observaciones=form.observaciones.data
            )
            flush()
        return redirect(url_for('otc.index'))
    return render_template('otc/create.html', form=form)

# Importar los módulos necesarios
from flask import Blueprint, render_template, request, redirect, url_for
from pony.orm import db_session
from .models import OrganismoTecnicoCriminologico, PersonaPrivadaDeLibertad
from .forms import OTCForm

# Crear el blueprint para las rutas relacionadas con OrganismoTecnicoCriminologico
routingOTC = Blueprint('otc', __name__)

# Definir la vista de edición de un registro en la tabla OrganismoTecnicoCriminologico
@routingOTC.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    # Obtener el objeto a actualizar y pasarle los datos al formulario
    otc = OrganismoTecnicoCriminologico[id]
    otc.id_persona_privada = otc.id_persona_privada.id_persona_privada
    form = OTCForm(obj=otc)

    # Si la solicitud es GET, mostrar la plantilla de edición con el formulario
    if request.method == 'GET':
        return render_template('otc/update.html', form=form, id=id)
    
    # Si la solicitud es POST y el formulario es válido, actualizar el registro en la base de datos y redirigir al usuario a la vista de índice
    elif request.method == 'POST'and form.validate_on_submit():
        with db_session:
            # Buscar el objeto PersonaPrivadaDeLibertad correspondiente al ID proporcionado en el formulario
            persona = PersonaPrivadaDeLibertad[form.id_persona_privada.data]

            # Actualizar los valores del registro con los valores proporcionados en el formulario
            otc.id_persona_privada = persona.id_persona_privada
            otc.fecha_evaluacion = form.fecha_evaluacion.data
            otc.riesgo = form.riesgo.data
            otc.observaciones = form.observaciones.data

            # Guardar los cambios en la base de datos y redirigir al usuario a la vista de índice
            db.commit()
            return redirect(url_for('otc.index'))


@routingOTC.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    otc = OrganismoTecnicoCriminologico[id]
    db.delete(otc)
    db.commit()
    return redirect(url_for('otc.index'))