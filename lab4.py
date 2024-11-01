from flask import Blueprint, render_template, redirect, request, session

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

@lab4.route('/lab4/add-form/')
def add_form():
    return render_template('lab4/add-form.html') 

@lab4.route('/lab4/mul-form/')
def mul_form():
    return render_template('lab4/mul-form.html') 

@lab4.route('/lab4/sub-form/')
def sub_form():
    return render_template('lab4/sub-form.html') 

@lab4.route('/lab4/pow-form/')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/add/', methods=['POST'])
def add():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0

    result = x1 + x2
    return render_template('lab4/add.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul/', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub/', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow/', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Нельзя возводить 0 в 0 степень!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count=0
@lab4.route('/lab4/tree/', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method=='GET':
        return render_template('lab4/tree.html', tree_count=tree_count) 
    operation = request.form.get('operation')
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree/')

users=[
    {'login': 'alex', 'password': '123'},
    {'login': 'bob', 'password': '555'},
    {'login': 'sofi', 'password': '111'},
    {'login': 'max', 'password': '222'},
    {'login': 'tony', 'password': '333'},
    {'login': 'mina', 'password': '321'},
    {'login': 'lily', 'password': '789'},
]

@lab4.route('/lab4/login/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        if 'login' in session:
            authorized=True
            login=session['login']
        else:
            authorized=False
            login=''
        return render_template('/lab4/login.html', authorized=authorized, login=login)

    login = request.form.get('login')
    password= request.form.get('password')
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login']= login
            return redirect('/lab4/login/')
            return render_template('/lab4/login.html', login=login, authorized=True)
    
    error='Неверный логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False)
    render_template('login.html') 

@lab4.route('/lab4/logout/', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login/')
   