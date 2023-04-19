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
    print(f"este es el formulariooooooooooooo {form.errors}")
    if request.method == 'GET':
        return render_template('otc/create.html', form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        with db_session:
            persona = PersonaPrivadaDeLibertad[form.id_persona_privada.data]
            otc = OrganismoTecnicoCriminologico(
                id_persona_privada=persona.id_persona_privada,
                fecha_evaluacion=form.fecha_evaluacion.data,
                riesgo=form.riesgo.data,
                observaciones=form.observaciones.data
            )
            db.commit()
            return redirect(url_for('otc.index'))
    elif request.method == 'POST' and not form.validate_on_submit():
        return f'formulario no valido {form.errors}'
@routingOTC.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    # obtener el objeto a actualizar y pasarle los datos al formulario
    otc = OrganismoTecnicoCriminologico[id]
    otc.id_persona_privada = otc.id_persona_privada.id_persona_privada
    form = OTCForm(obj=otc)

    if request.method == 'GET':
        return render_template('otc/update.html', form=form, id=id)
    elif request.method == 'POST'and form.validate_on_submit():
            with db_session:
                persona = PersonaPrivadaDeLibertad[form.id_persona_privada.data]
                otc.id_persona_privada = persona.id_persona_privada
                otc.fecha_evaluacion = form.fecha_evaluacion.data
                otc.riesgo = form.riesgo.data
                otc.observaciones = form.observaciones.data
                db.commit()
                return redirect(url_for('otc.index'))

@routingOTC.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    otc = OrganismoTecnicoCriminologico[id]
    db.delete(otc)
    db.commit()
    return redirect(url_for('otc.index'))