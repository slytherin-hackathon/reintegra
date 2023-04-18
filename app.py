from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required
from pony.flask import Pony
from database import *
from routes.ppl import routing
from routes.otc import routingOTC

# Configuración de la aplicación
UPLOAD_FOLDER = '/img/ppl'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Inicializacion de la app
app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    image_data = file.read()
    image = Image(filename=filename, image_data=image_data)
    db.commit()
    return 'Image uploaded successfully'

# URLS routing
app.register_blueprint( routing, url_prefix='/ppl')
app.register_blueprint( routingOTC, url_prefix='/otc')


#manejar el proceso de inicio de sesion y autenticacion de usuarios
login_manager = LoginManager(app)  
Pony(app)
#si un usuario no ha iniciado sesión y trata de acceder a una página protegida, será redirigido a la vista de inicio de sesión.
login_manager.login_view = 'login' 

#definir una funcion load_user. cuando necesita recuperar la información de un usuario para mostrar en la aplicación o para realizar comprobaciones de autenticación.
@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)


#Creo una ruta para el formulario de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        user = db.select('select * from User where username= $username and password=$password')
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

#Creo una ruta para la página principal de la aplicación, que solo puede ser accedida después de que el usuario haya iniciado sesión:
@app.route('/')
def index():
    if 'username' in session:
        return render_template('educacion-main.html', username=session['username'])
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
