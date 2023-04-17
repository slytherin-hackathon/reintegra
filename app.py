from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_required
from pony.orm import *

app = Flask(__name__)

# Set up SQLite database connection
db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

#defino una entidad 'User' con campos de nombre de usuario unico (no debe de haber repetido) y contrasenha
class User(db.Entity, UserMixin):
    username = Required(str, unique=True)
    email = Required(str)
    login = Required(str, unique=True)
    password = Required(str)

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
        username = request.form['nuevo Usuario']
        email = request.form['ingresar email']
        login = request.form['login']
        password = request.form['ingrese su còdigo']
        with db_session:
            user= User(username = username, password = password)
        return "Usuario registrado con èxito"
    return render_template('.html')
      
  



#Creo una ruta para el formulario de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        user = db.select('select * from User where username=$username and password=$password')
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
