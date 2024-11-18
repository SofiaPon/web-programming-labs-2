from flask import Blueprint, render_template, session, redirect, request, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash 
import sqlite3
from os import path

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
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kb',
            user='sofia_ponomareva_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()

    return conn, cur 

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



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
        if user is None or user['password'] != password:
            return render_template('lab5/login.html', error="Логин и/или пароль неверны")
        # Успешный вход
        session['login'] = login
        return render_template('lab5/success_login.html', login=login)
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка: {str(e)}')
    
    finally:
        # Закрытие курсора и соединения
        if cur:
            cur.close()
        if conn:
            conn.close()

@lab5.route('/lab5/create/', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login/')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn = None
    cur = None

    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))

        user = cur.fetchone()
        user_id = user["id"] if user else None
        
        if user_id is None:
            return redirect('/lab5/login/')
        
        if not title or not article_text:
            return render_template('lab5/create_article.html', error='Название и текст статьи не могут быть пустыми.')

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", (user_id, title, article_text))
        else:
            cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", (user_id, title, article_text))

        conn.commit()  # Зафиксировать изменения в базе данных

    except Exception as e:
        # Логирование ошибки для отладки
        current_app.logger.error(f"Error occurred: {e}")
        return render_template('lab5/create_article.html', error='Произошла ошибка при сохранении статьи.')
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return redirect('/lab5/')
    def create_article():
       current_app.logger.info("Запрос на создание статьи получен")
       db_type = current_app.config.get('DB_TYPE')
       if db_type is None:
           current_app.logger.error("DB_TYPE is not set in the configuration!")
           return "Ошибка: DB_TYPE не установлен", 500
       # Логика сохранения статьи здесь
       return "Статья успешно сохранена", 200

@lab5.route('/lab5/list/')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login/')

    conn, cur = db_connect()

    # Получение ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    # Получение статей пользователя с любимыми статьями первыми
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC;", (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur)

    # Проверка на отсутствие статей
    if not articles:
        message = "У вас пока нет статей."
    else:
        message = None

    return render_template('/lab5/articles.html', articles=articles, message=message)

@lab5.route('/lab5/logout/')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')

@lab5.route('/lab5/edit/<int:article_id>/', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login/')

    conn, cur = db_connect()

    if request.method == 'GET':
        # Получение статьи для редактирования
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return redirect('/lab5/list/')

        return render_template('lab5/edit_article.html', article=article)
    
    # Обновление статьи
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/edit_article.html', article={'id': article_id, 'title': title, 'article_text': article_text}, error="Название и текст статьи не должны быть пустыми")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list/')

@lab5.route('/lab5/delete/<int:article_id>/', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login/')

    conn, cur = db_connect()

    # Удаление статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list/')

@lab5.route('/lab5/users')
def users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login/')
    
    conn, cur = db_connect()

    # Получение всех логинов пользователей
    cur.execute("SELECT login FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)


