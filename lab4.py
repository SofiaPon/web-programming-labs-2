from flask import Blueprint, render_template, redirect, request 

lab4 = Blueprint('lab4', __name__)

@lab4.route("/index")
def start():
    return redirect('/menu', code=302)

@lab4.route("/menu")
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
        </ol>
        </main>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form/')
def div_form():
    return render_template('lab4/div-form.html') 

@lab4.route('/lab4/div/', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!') 

    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!') 

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)