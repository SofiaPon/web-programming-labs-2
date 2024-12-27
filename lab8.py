from flask import Blueprint, render_template, request, redirect, session
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab8_main():
    user = "anonymous"  # Пока пользователь анонимный
    return render_template('lab8/lab8.html', user=user)

@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    user = users.query.filter_by(login = login_form).first()
    if not login_form or not password_form:
        return render_template('lab8/login.html', error='Заполните все поля')
    
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember= False)
            return redirect('/lab8')
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
   if request.method == 'GET':
        return render_template('lab8/register.html')
    # Получение данных из формы
        login_form = request.form.get('login')
        password_form = request.form.get('password')
    # Проверки на пустые значения
        if not login_form or not password_form:
            return render_template('lab8/register.html', error='Поля логина и пароля обязательны')
    # Проверка существования пользователя с таким логином
        login_exists = users.query.filter_by(login=login_form).first()
        if login_exists:
            return render_template('lab8/register.html', error='Такой пользователь уже существует')
    # Хеширование пароля и добавление нового пользователя
        password_hash = generate_password_hash(password_form)
        new_user = users(login=login_form, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/lab8/')


@lab8.route('/create')
def create_article():
    return "Создать статью (в разработке)"

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

