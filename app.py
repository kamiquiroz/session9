import functools

from flask import Flask, render_template, request, flash, jsonify, redirect, g, url_for, session
from werkzeug.security import generate_password_hash

from forms import ContactUs
from message import mensajes

import yagmail as yagmail
import os

import utils

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)
from db import get_db

@app.route('/')
def index():
    if g.user:
        return redirect(url_for('send'))
    return render_template('login.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            db = get_db()
            error = None

            if not username:
                error = 'Debes ingresar un usuario'
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')

            user = db.execute('SELECT * FROM usuario WHERE usuario= ? AND contraseña= ?', (username, password)).fetchone()

            if user is None:
                error = 'Usuario o contraseña inválidos'
                flash(error)
            else:
                session.clear()
                session['user_id'] = user[0]

            db.close_db()

        return render_template('login.html')
    except Exception as ex:
        print(ex)
        return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    try:
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            error = None
            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('register.html')

            if not utils.isUsernameValid(username):
                error = "El usuario no es valido"
                flash(error)
                return render_template('register.html')

            if not utils.isPasswordValid(password):
                error = "El password no es valido"
                flash(error)
                return render_template('register.html')

            db = get_db()

            #generate_password_hash

            user = db.execute('SELECT id_usuario FROM usuario WHERE correo=?',(email,)).fetchone()

            if user is not None:
                error = 'El correo ya existe'.format(email)
                flash(error)
                return render_template('register.html')

            db.execute('INSERT INTO usuario (nombre, usuario, correo, contraseña) VALUES (?,?,?,?)',
                       (name, username, email, generate_password_hash(password)))

            db.commit()
            '''yag = yagmail.SMTP('mintic202221@gmail.com', 'Mintic2022')
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bievenido al portal de Registro de Vacunación  usa este link '
                              'para activar tu cuenta')

            flash("Revisa tu correo para activar tu cuenta")'''
            return render_template('login.html')

        return render_template('register.html')
    except Exception as e:
        print(e)
        return render_template('register.html')


@app.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    form = ContactUs()
    return render_template('contactUs.html', form=form)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view()


@app.route('/mensaje')
def message():
    return jsonify({'usuario': mensajes, 'mensaje': 'Mensajes'})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    if request.method == 'POST':
        from_id = g.user[0]
        to_username = request.form['para']
        subject = request.form['asunto']
        body = request.form['mensaje']

        if not to_username:
            flash('Campo requerido')
            return render_template('send.html')

        if not subject:
            flash('Campo requerido')
            return render_template('send.html')

        if not body:
            flash('Campo requerido')
            return render_template('send.html')

        db = get_db()
        user_to = db.execute('SELECT * FROM usuario WHERE usuario = ?', (to_username,)).fetchone()

        if user_to is None:
            error = 'No existe el usuario ingresado'
        else:

            db.execute('INSERT INTO mensajes (from_id, to_id, asunto, mensaje) VALUES (?,?,?,?)',
                       (from_id, user_to[0], subject, body))
            db.commit()
            db.close_db()
    return render_template('send.html')








if __name__ == '__main__':
    app.run()
