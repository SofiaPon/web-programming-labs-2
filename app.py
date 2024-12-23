import os
from flask import Flask, redirect, url_for
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres') 

app.secret_key= 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)

@app.route("/")
@app.route("/index")
def start():
    return redirect ('/menu', code=302)
@app.route("/menu")
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
            <li><a href="http://127.0.0.1:5000/lab1">Первая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab2'>Вторая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab3'>Третья лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab4/'>Четвертая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab5/'>Пятая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab6/'>Шестая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab7/'>Седьмая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab8/'>Восьмая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/rgz/'>РГЗ</a></li>
        <ol>
        </main>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""
