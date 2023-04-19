from flask import Blueprint, render_template, request, redirect, url_for
from database import * 
from forms import PSform

routingPS = Blueprint('ps', __name__)

@routingPS.route('/')
def index():
    ps_list = PlanSalidaLibertad.select()
    return render_template('ps/index.html', ps_list=ps_list)

 
@routingPS.route('/create', methods=['GET', 'POST'])
def create():
    form = PSform()
    
    if request.method == 'GET':
        return render_template('ps/create.html', form=form)
    elif request.method == "POST" and form.validate_on_submit():
        with db_session:
            form = PSform()
            persona = PersonaPrivadaDeLibertad[form.id_persona_privada.data]
            print({'persona': persona})
            ps = PlanSalidaLibertad(
                id_persona_privada=form.id_persona_privada.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_fin=form.fecha_fin.data,
                actividades=form.actividades.data,
                seguimiento=form.seguimiento.data,
                )

            flush()
        return redirect(url_for('ps.index'))
    elif request.method == 'POST':
        print(form.errors)
        return 'se ha cargado el formulario pero no se ha validado'
@routingPS.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    ps = PlanSalidaLibertad[id]
    ps.id_persona_privada = ps.id_persona_privada.id_persona_privada
    form = PSform(obj=ps)

    if request.method == 'GET':
        return render_template('ps/update.html', form=form, id=id)
    elif request.method == 'POST'and form.validate_on_submit():
            with db_session:
                persona = PersonaPrivadaDeLibertad[form.id_persona_privada.data]
                ps.id_persona_privada = persona.id_persona_privada
                ps.fecha_inicio = form.fecha_inicio.data
                ps.fecha_fin = form.fecha_fin.data
                ps.actividades = form.actividades.data
                ps.seguimiento = form.seguimiento.data
                db.commit()
                return redirect(url_for('ps.index'))

@routingPS.route('/delete/<id>')
def delete(id):
    ps = PlanSalidaLibertad[id]
    ps.delete()
    return redirect(url_for('ps.index'))