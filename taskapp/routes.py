import time

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from taskapp import app, db
from taskapp.models import User

menu = [{'name': 'Авторизация', 'url': 'login'},
        {'name': 'Страница для авторизованных пользователей', 'url': 'auth_page'}]

@app.route('/')
def index():
    if current_user.is_anonymous:
        username = 'Гость'
        return render_template('index.html', title='Главная страница', menu=menu, username=username)
    else:
        username = f"{current_user.name} {current_user.surname}"
        return render_template('index.html', title='Главная страница', menu=menu, username=username)


@app.route('/auth_page')
@login_required
def auth_page():
    return 'Вы зашли на закрытую страничку:)'


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        if request.form.get('name') and \
                request.form.get('surname') and\
                request.form.get('psw') and\
                request.form.get('psw'):
            try:
                name = request.form['name']
                surname = request.form['surname']
                login = request.form['login']
                psw = request.form['psw']
                db.session.add(User(name=name, surname=surname, psw=psw, login=login))
                db.session.commit()
                flash('Регистрация прошла успешно!')
                return redirect('/')
            except IntegrityError:
                flash('Пользователь с таким логином уже существует!')
                return render_template('index.html', title='Главная страница', menu=menu)
        else:
            flash('Заполните, пожалуйста, все поля!')
            return render_template('index.html', title='Главная страница', menu=menu)
    return render_template('login_form.html', title='Главная страница', menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        if not current_user.is_anonymous:
            return redirect('/')
    if request.method == 'POST':
        login = request.form['login']
        psw = request.form['psw']
        if login and psw:
            user = User.query.filter_by(login=login).first()
            if not user:
                flash('Пользователь с указанным логином не найден!')
                return render_template('login_form.html', title='Авторизация', reg_url=url_for('index'))
            if user and psw == user.psw:
                login_user(user)
                return redirect('/')
            else:
                flash('Логин или пароль указан неверно!')
                return render_template('login_form.html', title='Авторизация', reg_url=url_for('index'))
        else:
            flash('Не все поля заполнены!')
    return render_template('login_form.html', title='Главная страница', reg_url=url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(401)
def error_401(error):
    return render_template('page401.html', url=url_for('index'), title='Ошибка доступа')

