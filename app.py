from flask import Flask, redirect
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect ('/menu', code=302)


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

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
            <li><a href='http://127.0.0.1:5000/lab2'>Вторая лабораторная</a></li>
            <li><a href='http://127.0.0.1:5000/lab3'>Третья лабораторная</a></li>
        <ol>
        </main>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
