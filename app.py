from flask import Flask, render_template, request, flash
from forms import ContactUs

import yagmail as yagmail
import os

import utils

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)


@app.route('/')
def index():
    return render_template('sesion.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # validamos hasta aqui
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

            yag = yagmail.SMTP('mintic202221@gmail.com', 'Mintic2022')
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bievenido al portal de Registro de Vacunación  usa este link '
                              'para activar tu cuenta')

            flash("Revisa tu correo para activar tu cuenta")
            return render_template('login.html')

        return render_template('register.html')
    except Exception as e:
        print(e)
        return render_template('register.html')


@app.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    form = ContactUs()
    return render_template('contactUs.html', form=form)


if __name__ == '__main__':
    app.run()
