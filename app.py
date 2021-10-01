from flask import Flask, render_template, request, flash

import yagmail as yagmail

import utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sesion.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods = ('GET', 'POST'))
def register():
    print(1)
    try:
        if request.method == 'POST':
            print(2)
            username = request.form['username']
            print(username)
            password = request.form['password']
            print(password)
            email = request.form['email']
            print(email)

            #validamos hasta aqui
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

            return render_template('login.html')
        return render_template('register.html')
    except Exception as e:
        return render_template('register.html')

if __name__ == '__main__':
    app.run()
