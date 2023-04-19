from flask import Blueprint, render_template, request, redirect, url_for
from database import *
from forms import PersonaForm

routing = Blueprint('ppl', __name__)

# CRUD operations
@routing.route('/', methods = ['GET'])
def index():
    personas = select(p for p in PersonaPrivadaDeLibertad)
    return render_template('ppl/index.html', personas=personas)

@routing.route('/create', methods=['GET', 'POST'])
def create():
    form = PersonaForm()
    if request.method == 'POST'and form.validate_on_submit():
            persona = PersonaPrivadaDeLibertad(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                genero=form.genero.data,
                documento_identidad=form.documento_identidad.data,
                fecha_de_ingreso=form.fecha_de_ingreso.data,
                fecha_de_salida=form.fecha_de_salida.data,
                descripcion=form.descripcion.data
            )
            db.commit()
            print({'persona': persona.to_dict()})
            return redirect(url_for('ppl.index'))
    elif request.method == 'GET':
        return render_template('ppl/create.html', form=form)
    elif request.method == 'POST' and not form.validate_on_submit():
        return render_template('ppl/create.html', form=form)

@routing.route('/edit/<persona_id>', methods=['GET', 'POST'])
def edit(persona_id):
    print('persona_id: ', persona_id)

    persona = PersonaPrivadaDeLibertad.get(id_persona_privada=persona_id)
    print('persona: ', persona)
    form = PersonaForm(obj=persona)
    if request.method == 'POST':
        if form.validate_on_submit():
            persona.set(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                genero=form.genero.data,
                documento_identidad=form.documento_identidad.data,
                # fotografia=form.fotografia.data
            )
            db.commit()
            return redirect(url_for('ppl.index'))
    return render_template('ppl/update.html', form=form, persona=persona)

@routing.route('/delete/<persona_id>', methods=['POST'])
def delete(persona_id):
    persona = PersonaPrivadaDeLibertad.get(id_persona_privada=persona_id)
    persona.delete()
    db.commit()
    return redirect(url_for('ppl.index'))