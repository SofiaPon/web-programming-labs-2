from flask import Blueprint, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash 

lab5 = Blueprint('lab5', __name__)

@lab5.route("/index")
def start():
    return redirect('/menu', code=302)

@lab5.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ ФБ Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
        <ol>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href='/lab2'>Вторая лабораторная</a></li>
            <li><a href='/lab3'>Третья лабораторная</a></li>
            <li><a href='/lab4'>Четвертая лабораторная</a></li>
            <li><a href='/lab5'>Пятая лабораторная</a></li>
        </ol>
        </main>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    conn = psycopg2.connect(
    host='127.0.0.1',
    database='kb',
    user='sofia_ponomareva_knowledge_base',
    password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur 

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

    return render_template('lab5/lab5.html', login=session.get('login'))


@lab5.route('/lab5/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')  # Отображаем форму регистрации

    # Обработка данных формы при методе POST
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab5/register.html', error="Заполните все поля")

    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='sofia_ponomareva_knowledge_base',
            user='sofia_ponomareva_knowledge_base',
            password='123'
        )
        cur = conn.cursor()

        # Проверка на существование пользователя
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        if cur.fetchone():
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        # Если пользователя нет, добавляем нового пользователя
        password_hash = generate_password_hash(password)   
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
        conn.commit()
        
        return render_template('lab5/success.html', login=login)

    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка: {str(e)}')
    
    finally:
        # Закрытие курсора и соединения
        if cur:
            cur.close()
        if conn:
            conn.close()


@lab5.route('/lab5/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на заполненность полей
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")
    
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='sofia_ponomareva_knowledge_base',
            user='sofia_ponomareva_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    
        # Используем параметризованный запрос
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        # Проверка существования пользователя
        if user is None or check_password_hash(user['password'] != password):
            return render_template('lab5/login.html', error="Логин и/или пароль неверны")

        # Успешный вход
        session['login'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)

    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка: {str(e)}')
    
    finally:
        # Закрытие курсора и соединения
        if cur:
            cur.close()
        if conn:
            conn.close()


