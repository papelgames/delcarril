#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash, g
import forms
from flask_wtf import CsrfProtect
from config import DevelopmentConfig
import json

from models import db, User, Comment

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()

def generate_session(username, user_id):
	session['user_id'] = user_id
	session['username'] = username

def paginado (pagina_actual, direccion):
    if pagina_actual <> 1 and direccion == 'menos':
        return pagina_actual - 1
    elif direccion == 'mas':
        return pagina_actual + 1

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in['login','create']:
        return redirect(url_for('index'))

@app.after_request
def after_request(response):

    return response

@app.route('/', methods = ['GET','POST'])
def index ():
    if 'username' in session:
        username = session['username']
        #user_id = session['user_id']
    custome_cookie = request.cookies.get('custom_cookie','indefinida')
    
    success_message = 'Estas en el index'
    flash(success_message)
    return render_template('index.html')

@app.route('/comment', methods = ['GET','POST'])
def comment ():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        user_id = session['user_id']
        print user_id

        comment = Comment(user_id = user_id,
                          text = comment_form.comment.data)
        
        db.session.add(comment)
        db.session.commit()

        success_message = 'El comentario se ha creado satisfactoriamente'
        flash(success_message)
    return render_template('comment.html', form = comment_form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    #<form id="login-form" method="POST"> 
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            generate_session(user.username, user.id)

            
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            return redirect( url_for('index'))

        else:
            error_message = u'Contraseña o usuario no válida'
            flash(error_message)
        
    return render_template('login.html', form = login_form)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        user = User (create_form.username.data,
                    create_form.email.data,
                    create_form.password.data)
        
        db.session.add(user)
        db.session.commit()

        success_message = 'Usuario registrado'
        flash(success_message)
       
    return render_template('create.html', formu = create_form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/paginas', methods=['GET'])
@app.route('/paginas/<int:page>', methods=['GET'])
def paginas(page = 1):
    per_page = 3
    
    next_page = paginado(page, 'mas')
    pre_page = paginado(page, 'menos')

    comments = Comment.query.join(User).add_columns(
                                    User.username,
                                    Comment.text).paginate(page,per_page,False)
    return render_template('paginas.html', comments = comments, pre_page = pre_page, next_page = next_page)


@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('custom_cookie', 'chota')
    return response

@app.route('/ajax-login', methods = ['POST'])
def ajax_login():
    print request.form
    username = request.form['username'];
    response ={'status': 200, 'username': username , 'id': 1}
    return json.dumps(response)

@app.route('/params')
#http://localhost:5000/params?params1=jose
def params ():
    param = request.args.get('params1','el no contiene parametros')
    return 'El parametros es : {}'.format(param) 

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()