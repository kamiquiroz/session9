from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ContactUs(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(message='Este campo es obligatorio')])
    email = EmailField('Correo', validators=[DataRequired(message='Este campo es obligatorio')])
    message = TextAreaField('Mensaje', validators=[DataRequired(message='Este campo es obligatorio')])
    send = SubmitField('Enviar Mensaje')