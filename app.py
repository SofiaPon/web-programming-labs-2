from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return """
<!doctype html>
<html>
    <head>
        <tittle>Пономарева София Александровна, Лабораторная 1</tittle>
    </head>
    <body>
        <header>
        НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""   

@app. route("/menu")
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
        <ol>
        </main>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Пономарева София Александровна, Лабораторная работа 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>
        <h1>web-сервер на flask</h1>
        <p>
            Flask - фреймворк для создания веб-приложений на языке программирования 
            Python, использующий набор инструментов Werkzeug, a также шаблонизатор 
            Jinja2. Относится к категории так называемых микрофреймворков - 
            минималистичных каркасов веб-приложений, сознательно предоставляющих 
            лишь самые базовые возможности.
        </p>
        <p>
            <a href="http://127.0.0.1:5000/menu">Меню</a>
        </p>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""