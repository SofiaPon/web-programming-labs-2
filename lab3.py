from flask import Blueprint, render_template, redirect, request, make_response

lab3 = Blueprint('lab3', __name__)

@lab3.route("/index")
def start():
    return redirect('/menu', code=302)

@lab3.route("/menu")
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
        </ol>
        </main>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color=request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color= name_color)

@lab3.route('/lab3/cookie/')
def cookie():
    resp=make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5) 
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie/')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name') 
    resp.delete_cookie('age') 
    resp.delete_cookie('name_color')
    return resp