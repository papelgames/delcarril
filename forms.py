#-*- coding: utf-8 -*-
from wtforms import Form, StringField, TextField, validators, PasswordField, IntegerField
from wtforms.fields.html5 import EmailField
from models import User

class CommentForm (Form):
    
    comment = TextField('comentario')
    user_id = IntegerField('user_id')

class IndexForm (Form):
    pass

class LoginForm(Form):
    username = StringField('Usuario',[
        validators.Required(message= 'El usuario no puede estar vacio.'), 
        validators.length(min=1,max= 10,message="El usuario no es valido")
    ])
    password = PasswordField(u'Contraseña',[
        validators.Required(message= 'La password no puede estar vacio.'), 
        validators.length(min=1,max= 10,message="El usuario no es valido")
    ])

class CreateForm(Form):
    username = StringField('Usuario',[
        validators.Required(message= 'El usuario no puede estar vacio.'), 
        validators.length(min=1,max= 10,message="El usuario no es valido")
    ])
    email = EmailField ('Correo electronico',
    [
        validators.Required(message= 'El email no puede estar vacio.'), 
       
    ])
    password = PasswordField('Contrasenia',[
        validators.Required(message= 'La password no puede estar vacio.'), 
        validators.length(min=1,max= 66 ,message="El usuario no es valido")
    ])
    def validate_username (form,field) :
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('El user ya existe')
