from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)



@app.route("/")
@app.route("/index")
def start():
    return redirect ('/menu', code=302)


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
        <p>
            <a href="http://127.0.0.1:5000/lab1/oak">Дуб</a>
        </p>
        <p>
            <a href="http://127.0.0.1:5000/lab1/student">Студент</a>
        </p>
        <p>    
            <a href="http://127.0.0.1:5000/lab1/BMW">БМВ М8</a>
        </p>
        <footer>
            &copy; Пономарева София, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route('/lab1/oak')
def oak():
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='lab1.css')}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{url_for('static', filename='oak.jpg')}">
    </body>
</html>
'''


@app.route("/lab1/student")
def student():
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='lab1.css')}">
    </head>
    <body>
        <h1>Пономарева София Александровна</h1>
        <img src="{url_for('static', filename='Логотип.png')}" width="300" height="200">
    </body>
</html>
'''

@app.route("/lab1/python")
def python():
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='lab1.css')}">
    </head>
    <body>
        <h1>Python</h1>
        <p>
            Python — это высокоуровневый язык программирования, отличающийся эффективностью, 
            простотой и универсальностью использования. Он широко применяется в разработке 
            веб-приложений и прикладного программного обеспечения, а также в машинном обучении и 
            обработке больших данных. За счет простого и интуитивно понятного синтаксиса является 
            одним из распространенных языков для обучения программированию. 
        </p>
        <p>
            Язык программирования Python был создан в 1989–1991 годах голландским программистом Гвидо 
            ван Россумом. Изначально это был любительский проект: разработчик начал работу над ним, 
            просто чтобы занять себя на рождественских каникулах. Хотя сама идея создания нового языка 
            появилась у него двумя годами ранее.
        </p>
        <p>
            Имя ему Гвидо взял из своей любимой развлекательной передачи «Летающий цирк Монти Пайтона». 
            Язык программирования он и выбрал — Python, что это означало название комик-группы. Это шоу 
            было весьма популярным среди программистов, которые находили в нем параллели с миром компьютерных технологий.
        </p>
        <img src="{url_for('static', filename='Питон.png')}" width="300" height="200">
    </body>
</html>
'''

@app.route("/lab1/BMW")
def BMW():
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="*** + url_for("static", filename="lab1.css") + *
    </head>
    <body>
        <h1>BMW M8 Competition, BMW M8 Coupe и BMW M850i xDrive Coupe</h1>
    <p>
        Автомобили M BMW 8 серии Coupe доставят Вам максимальное удовольствие от вождения в 
        атмосфере спортивного стиля и роскоши как на дорогах, так и на гоночной трассе:
        BMW M8 Competition Coupe и BMW M8 Coupe сочетают в себе гены M с высочайшей эксклюзивностью.
        BMW M850i xDrive Coupe впечатляет уникальным синтезом комфорта, динамики и эффективности.
    </p>
    <p>
        Последняя модификация 8- цилиндрового бензинового двигателя М TwinPower Turbo гарантирует 
        высокую динамику в соответствии с самыми современными стандартами. Этот высокооборотистый 
        агрегат развивает мощность 625 л.с. (460 кВт). Два турбонагнетателя отличаются оптимальной 
        приемистостью благодаря выпускному коллектору с поперечным расположением цилиндров. Этот 
        двигатель V8 также рассчитан на экстремальные нагрузки на гоночнойтрассе.
    </p>
    <p>
        Система полного привода M xDrive с активным дифференциалом М гарантирует максимальное 
        сцепление с дорожной поверхностью и высочайшую динамику как при повседневной эксплуатации, 
        так и на гоночных трассах. Уникальная технология М сочетает в себе маневренность, характерную 
        длязаднеприводной компоновки, с управляемостью, присущей полноприводным автомобилям. Вы можете 
        выбрать один из трех режимов движения: 4WD, 4WD Sport и - при отключенной DSC - 2WD.
    </p>
    <img src="{url_for('static', filename='БМВ.jpg')}" width="300" height="200">
    </body>
</html>
'''


@app.route('/lab2/example')
def example():
    name= 'София Пономарева'
    lab_number2 = '2'
    group = 'ФБИ-23'
    course = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321},
        ]
    return render_template('example.html', name=name, lab_number2=lab_number2, group=group, course=course, fruits=fruits)
    

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')
    

@app.route('/lab2/books')
def books():   
    name = 'София Пономарева'
    lab_number2 = '2'
    group = 'ФБИ-23'
    course = '3'   
    books = [
        {"author": "Харуки Мураками", "title": "Кафка на пляже ", "genre": "Роман", "pages": 672},
        {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Классика", "pages": 671},
        {"author": "Лев Толстой", "title": "Война и мир", "genre": "Классика", "pages": 1225},
        {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
        {"author": "Рей Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Фантастика", "pages": 249},
        {"author": "Харуки Мураками", "title": "Норвежский лес", "genre": "Роман", "pages": 384},
        {"author": "Харуки Мураками", "title": "Мой любимый sputnik", "genre": "Роман", "pages": 272},
        {"author": "Джоан Роулинг", "title": "Гарри Поттер", "genre": "Роман", "pages": 432},
        {"author": "Виктор Пелевин", "title": "Круть", "genre": "Фантастика", "pages": 324},
        {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 560}
    ]

    return render_template('books.html', name=name, lab_number2=lab_number2, group=group, course=course, books=books)


@app.route('/lab2/cars/')
def cars():
    name = 'София Пономарева'
    lab_number2 = '2'
    group = 'ФБИ-23'
    course = '3'
    cars=[
        {"name": "Bugatti La Voiture Noire", "description": "В 2019 компания Bugatti представила модель La Voiture Noire, построенную на основе Chiron. Кузов изготовлен из углеродного волокна и имеет оригинальный дизайн с удлиненными передней и задней частью. Автомобиль оснащен двигателем от Chiron и 7-скоростной АКПП с системой полного привода. В целом настройки шасси и трансмиссии ориентированы на больший уровень комфорта. Стать владельцем La Voiture Noire можно за 18,7 млн долларов.",
         "image": "1 машина.jpeg"},
        {"name": "Pagani Zonda HP Barchetta", "description": "Автомобиль представлен в 2017 г., разработка была приурочена к 60-летнему юбилею основателя компании Pagani. Машина имеет оригинальный открытый кузов и оснащена двигателем Mercedes-Benz объемом 7,3 л, развивающим 800 сил и имеющим крутящий момент 850 Н*м. Всего было выпущено 3 экземпляра автомобиля, из которых два передали клиентам компании, а один остался в личной коллекции владельца Pagani. Цена машины на момент выхода составляла 17,6 млн. долларов, нынешняя цена будет явно выше. Модификация HP Barchetta ознаменовала завершение выпуска модели Zonda.", 
        "image": "2 машина.jpeg"},
        {"name": "Bugatti Chiron Profilée", "description": "В десятку самых дорогих автомобилей попала еще одна модификация Bugatti Chiron – Profilée, изготовленная в конце 2022 г. на базе Chiron Pur Sport. Машина отличается другим обвесом кузова, настройками коробки передач и подвески. В результате удалось улучшить динамику разгона, а максимальная скорость составляет 380 км/ч. Изначально планировалось собрать 30 машин, однако впоследствии проект закрыли из-за распределения всех заказов на лимитированную модель Chiron. Всего был построен один экземпляр, который продали в начале 2023 г. на аукционе RM Sotheby's за почти 9,8 млн фунтов (эквивалентно 10,78 млн долларов).", 
        "image": "3 машина.jpeg"},
        {"name": "777 Hypercar", "description": "В середине 2023 г. небольшая итальянская компания 777 Motors из Монцы представила первый образец автомобиля 777 Hypercar. Фактически проект разрабатывался группой сторонних фирм, поскольку 777 Motors не имеет опыта создания автомобилей. Машина соответствует гоночной категории LMP1 и не предназначена для эксплуатации на дорогах общего пользования. Силовой агрегат включает в себя 730-сильный бензиновый двигатель от фирмы Gibson Technology и позволяет разогнать автомобиль до 370 км/ч. Старт продаж запланирован на 2025 г. по цене не менее 7,6 млн долларов, которая может измениться в любую сторону.", 
        "image": "4 машина.jpeg"},
        {"name": "Bugatti Divo", "description": "Замыкает рейтинг из 12 самых дорогих автомобилей в мире, Bugatti Divo, выпускавшийся с 2019 по 2021 гг. Всего было собрано 40 экземпляров, оснащенных двигателем мощностью 1500 сил. Мотор является хорошо известным любителям Bugatti 16-цилиндровым W-образным агрегатом объемом 8 л с двойным турбонаддувом. Машина создана для трековых гонок и получила название в честь французского гонщика Альберта Диво, выступавшего за Bugatti в 20-х гг. прошлого века в гонках «Тарга Флорио». Специфика автомобиля потребовала улучшения аэродинамики и снижения веса за счет широкого использования углепластика в отделке салона.", 
        "image": "5 машина.jpeg"}
    ]

    return render_template('cars.html', name=name, lab_number2=lab_number2, group=group, course=course, cars=cars)