from flask import Blueprint, render_template, redirect

lab2 = Blueprint('lab2', __name__)

@lab2.route("/index")
def start():
    return redirect('/menu', code=302)

@lab2.route("/menu")
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

@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')

@lab2.route('/lab2/example/')
def example():
    
    name = 'София Пономарева'
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

    return render_template('lab2/example.html', name=name, lab_number2=lab_number2, group=group, course=course, fruits=fruits)

@lab2.route('/lab2/books/')
def books():

    name = 'София Пономарева'
    lab_number2 = '2'
    group = 'ФБИ-23'
    course = '3'
    books = [
        {"author": "Харуки Мураками", "title": "Кафка на пляже", "genre": "Роман", "pages": 672},
        {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Классика", "pages": 671},
        {"author": "Лев Толстой", "title": "Война и мир", "genre": "Классика", "pages": 1225},
        {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
        {"author": "Рей Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Фантастика", "pages": 249},
        {"author": "Харуки Мураками", "title": "Норвежский лес", "genre": "Роман", "pages": 384},
        {"author": "Джоан Роулинг", "title": "Гарри Поттер", "genre": "Роман", "pages": 432},
        {"author": "Виктор Пелевин", "title": "Круть", "genre": "Фантастика", "pages": 324},
        {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 560}
    ]

    return render_template('lab2/books.html', name=name, lab_number2=lab_number2, group=group, course=course, books=books)

@lab2.route('/lab2/cars/')
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

    return render_template('lab2/cars.html', name=name, lab_number2=lab_number2, group=group, course=course, cars=cars)