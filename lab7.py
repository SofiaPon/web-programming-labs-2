from flask import Blueprint, render_template, request, redirect, session, abort

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7')
def main():
    return render_template('lab7/lab7.html')

films= [
        {
            "tittle": 'Tenet',
            "tittle_ru": 'Довод',
            "year": 2020,
            "descriprion": 'После теракта в киевском оперном театре агент ЦРУ объединяется с \
            британской разведкой, чтобы противостоять русскому олигарху, который сколотил \
            состояние на торговле оружием. Для этого агенты используют инверсию времени — \
            технологию будущего, позволяющую времени идти вспять.'

        },

         {
            "tittle": 'Ready Player One',
            "tittle_ru": 'Первому игроку приготовиться',
            "year": 2018,
            "descriprion": 'Действие фильма происходит в 2045 году, мир погружается в хаос и \
            находится на грани коллапса. Люди ищут спасения в игре OASIS – огромной вселенной \
            виртуальной реальности. Ее создатель, гениальный и эксцентричный Джеймс Холлидэй, \
            оставляет уникальное завещание. Все его колоссальное состояние получит игрок, первым \
            обнаруживший цифровое «пасхальное яйцо», которое миллиардер спрятал где-то на просторах \
            OASISа. Запущенный им квест охватывает весь мир. Совершенно негероический парень по имени \
            Уэйд Уоттс решает принять участие в состязании, с головой бросаясь в головокружительную, \
            искажающую реальность погоню за сокровищами по фантастической вселенной, полной загадок, \
            открытий и опасностей.'

        },

         {
            "tittle": 'The Batman',
            "tittle_ru": 'Бэтмен',
            "year": 2022,
            "descriprion": 'После двух лет поисков правосудия на улицах Готэма Бэтмен становится \
            для горожан олицетворением беспощадного возмездия. Когда в городе происходит серия \
            жестоких нападений на высокопоставленных чиновников, улики приводят Брюса Уэйна в \
            самые тёмные закоулки преступного мира, где он встречает Женщину-Кошку, Пингвина, \
            Кармайна Фальконе и Загадочника. Теперь под прицелом оказывается сам Бэтмен, которому \
            предстоит отличить друга от врага и восстановить справедливость во имя Готэма.'

        },

         {
            "tittle": 'Catwoman',
            "tittle_ru": 'Женщина-кошка',
            "year": 2004,
            "descriprion": 'Пейшинс Филипс работает дизайнером в крупной косметической компании, \
            которая готовится выпустить на рынок новый продукт, замедляющий старение. Но у этой \
            революционной новинки есть существенный недостаток, который компания тщательно скрывает \
            и о котором случайно узнает Пэйшинс. Дальнейшие события меняют ее жизнь самым невероятным образом...'

        },

        {
            "tittle": 'Отряд самоубийц',
            "tittle_ru": 'Suicide Squad',
            "year": 2016,
            "descriprion": 'Правительство решает дать команде суперзлодеев шанс на искупление. \
            Подвох в том, что их отправляют на выполнение миссии, где они, вероятнее всего, погибнут.'

        },
    ]
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET']) 
def get_film(id):
    # Проверка на принадлежность id диапазону
    if id < 0 or id >= len(films):
        abort(404)  # Возвращаем ошибку 404 если индекс неверный
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE']) 
def del_film(id):
    # Проверяем, находится ли ID в допустимом диапазоне
    if 0 <= id < len(films):
        del films[id]  # Удаляем фильм с заданным ID
        return '', 204  # Возвращаем пустой ответ с кодом 204 No Content
    else:
        # Если ID не корректен, возвращаем ошибку 404
        abort(404, description="Фильм с таким ID не найден")


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT']) 
def put_film(id):
    if id < 0 or id >= len(films):
        return '', 404
    film = request.get_json()
    films[id]=film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film or not all(key in film for key in ["title", "title_ru", "year", "description"]):
        abort(400, description="Неполные данные фильма. Ожидаются: title, title_ru, year, description")
    films.append(film)
    return jsonify({"id": len(films) - 1}), 201



