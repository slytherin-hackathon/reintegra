from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_required
from pony.orm import *
from datetime import date

app = Flask(__name__)
app.secret_key = ('esto_no_es_secreto')  #establezco una 'clave secreta'

# Set up SQLite database connection
db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

#defino una entidad 'User' con campos de nombre de usuario unico (no debe de haber repetido) y contrasenha
class User(db.Entity, UserMixin):
    username = Required(str, unique=True)
    email = Required(str)
    #login = Required(str, unique=True)
    password = Required(str)

#defino una entida 'ReportePSicologico'
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

login_manager = LoginManager(app)  #manejar el proceso de inicio de sesion y autenticacion de usuarios
login_manager.login_view = 'login' #si un usuario no ha iniciado sesión y trata de acceder a una página protegida, será redirigido a la vista de inicio de sesión.


#definir una funcion load_user. cuando necesita recuperar la información de un usuario para mostrar en la aplicación o para realizar comprobaciones de autenticación.
@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)

# Crear una ruta para el formulario de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        username = request.form['name']
        email = request.form['email']
        #login = request.form['login']
        password = request.form['password']
        with db_session:
            user= User(username = username, password = password, email=email)
        return "Usuario registrado con èxito"
    else:
        return render_template('signup.html')
      

#Creo una ruta para el formulario de login
@app.route('/login', methods=['GET', 'POST'])
@db_session()
def login():
    if request.method == 'POST':
        email = request.form['email']
        #username = request.form['usuario']
        password = request.form['password']
        email = db.select('select * from User where email=$email and password=$password',{'email': email, 'password': password})
        if email:
            session['email'] = email
            return redirect(url_for('index'))
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


#Creo una ruta para la página principal de la aplicación, que solo puede ser accedida después de que el usuario haya iniciado sesión:
@app.route('/')
def index():
    if 'email' in session:
        return render_template('educacion-main3.html', email=session['email'])
    else:
        return redirect(url_for('login'))


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

