from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path
from datetime import datetime

rgz = Blueprint('rgz', __name__)

ADMIN_USER = 'Smailik'


# Функции подключения к базе данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        try:
            conn = psycopg2.connect(
                dbname="Smailik",
                user="Smailik",
                password="212121",
                host="127.0.0.1"
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            return None, None
    else:
        try:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения к SQLite: {e}")
            return None, None

    return conn, cur


def db_close(conn, cur):
    if conn and cur:
        conn.commit()
        cur.close()
        conn.close()


# Декораторы для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('rgz.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('login') != ADMIN_USER:
            return redirect(url_for('rgz.main'))
        return f(*args, **kwargs)
    return decorated_function


def guest_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' in session:
            return redirect(url_for('rgz.main'))
        return f(*args, **kwargs)
    return decorated_function


# Маршруты
@rgz.route('/rgz/register', methods=['GET', 'POST'])
@guest_required
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return redirect(url_for('rgz.login'))


@rgz.route('/rgz/login', methods=['GET', 'POST'])
@guest_required
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/login.html', error="Заполните поля")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    session['login_id'] = user['id']
    db_close(conn, cur)
    return redirect(url_for('rgz.main'))


@rgz.route('/rgz/logout')
@login_required
def logout():
    session.pop('login', None)
    return redirect(url_for('rgz.login'))


@rgz.route('/rgz/')
def main():
    user = session.get('login')
    if not user:
        return render_template('rgz/rgz.html')

    if user == ADMIN_USER:
        return render_template('rgz/admin.html')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('rgz/user_list.html', users=users)


@rgz.route('/rgz/admin/users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('rgz/manage_users.html', users=users)


@rgz.route('/rgz/admin/api', methods=['POST'])
@admin_required
def admin_api():
    """
    Основной маршрут JSON-RPC API для управления пользователями.
    Ожидает запрос в формате JSON-RPC.
    """
    try:
        data = request.get_json()

        # Проверяем структуру JSON-RPC
        if 'jsonrpc' not in data or data['jsonrpc'] != '2.0' or 'method' not in data or 'id' not in data:
            raise ValueError("Неверный формат JSON-RPC")

        method = data['method']
        params = data.get('params', {})

        # Маршрутизируем вызов метода
        if method == 'delete_user':
            result = delete_user_api(params)
        elif method == 'edit_user':
            result = edit_user_api(params)
        else:
            raise ValueError("Неизвестный метод")

        return jsonify({"jsonrpc": "2.0", "result": result, "id": data['id']})

    except ValueError as e:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32602, "message": str(e)}, "id": data.get('id', None)}), 400
    except Exception as e:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32603, "message": "Ошибка сервера"}, "id": data.get('id', None)}), 500


def delete_user_api(params):
    """
    Удаляет пользователя по ID через JSON-RPC.
    """
    user_id = params.get('user_id')
    if not user_id:
        raise ValueError("user_id не указан")

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM users WHERE id=%s;", (user_id,))
        else:
            cur.execute("DELETE FROM users WHERE id=?;", (user_id,))

        conn.commit()
        return {"message": "Пользователь успешно удалён."}
    except Exception as e:
        raise ValueError(f"Ошибка при удалении пользователя: {e}")
    finally:
        db_close(conn, cur)


def edit_user_api(params):
    """
    Редактирует пользователя по ID через JSON-RPC.
    """
    user_id = params.get('user_id')
    new_login = params.get('login')
    new_password = params.get('password')

    if not user_id or not new_login:
        raise ValueError("user_id и login обязательны")

    password_hash = generate_password_hash(new_password) if new_password else None

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            if password_hash:
                cur.execute("UPDATE users SET login=%s, password=%s WHERE id=%s;", (new_login, password_hash, user_id))
            else:
                cur.execute("UPDATE users SET login=%s WHERE id=%s;", (new_login, user_id))
        else:
            if password_hash:
                cur.execute("UPDATE users SET login=?, password=? WHERE id=?;", (new_login, password_hash, user_id))
            else:
                cur.execute("UPDATE users SET login=? WHERE id=?;", (new_login, user_id))

        conn.commit()
        return {"message": "Пользователь успешно обновлён."}
    except Exception as e:
        raise ValueError(f"Ошибка при редактировании пользователя: {e}")
    finally:
        db_close(conn, cur)

# Получение списка пользователей через JSON-RPC
@rgz.route('/rgz/users', methods=['POST'])
def user_list():
    try:
        data = request.get_json()

        # Проверяем корректность запроса
        if not data or data.get('method') != 'get_user_list':
            return jsonify({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32600,
                    "message": "Invalid Request"
                },
                "id": data.get("id") if data else None
            }), 400

        conn, cur = db_connect()

        # Получаем список пользователей
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, login FROM users;")
        else:
            cur.execute("SELECT id, login FROM users;")

        users = cur.fetchall()
        db_close(conn, cur)

        # Преобразуем результаты в JSON-совместимый формат
        users_list = [{'id': user['id'], 'login': user['login']} for user in users]

        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "users": users_list
            },
            "id": data.get("id")
        })
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32000,
                "message": f"Server error: {str(e)}"
            },
            "id": None
        }), 500



def get_user_list(params):
    current_user = session.get('login')
    conn, cur = db_connect()

    # Получаем список пользователей, кроме текущего и администратора
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login FROM users WHERE login != %s AND login != %s;", (current_user, ADMIN_USER))
    else:
        cur.execute("SELECT id, login FROM users WHERE login != ? AND login != ?;", (current_user, ADMIN_USER))

    users = cur.fetchall()
    db_close(conn, cur)

    return {'status': 'success', 'users': users}


@rgz.route('/rgz/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    current_user = session.get('login')
    conn, cur = db_connect()

    # Получение ID и имени текущего пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login FROM users WHERE login = %s;", (current_user,))
    else:
        cur.execute("SELECT id, login FROM users WHERE login = ?;", (current_user,))
    current_user_data = cur.fetchone()
    if not current_user_data:
        return jsonify({'status': 'error', 'message': 'Пользователь не найден'}), 400
    sender_id = current_user_data['id']
    current_user_name = current_user_data['login']

    # Получение имени получателя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE id = %s;", (user_id,))
    else:
        cur.execute("SELECT login FROM users WHERE id = ?;", (user_id,))
    receiver_data = cur.fetchone()
    if not receiver_data:
        return jsonify({'status': 'error', 'message': 'Получатель не найден'}), 400
    receiver_name = receiver_data['login']

    if request.method == 'POST':
        try:
            message_text = request.json.get('message')
            if not message_text:
                return jsonify({'status': 'error', 'message': 'Сообщение не может быть пустым'}), 400
            timestamp = datetime.now()

            # Добавление сообщения в базу данных
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    INSERT INTO messages (sender_id, receiver_id, message_text, timestamp, is_deleted)
                    VALUES (%s, %s, %s, %s, %s);
                """, (sender_id, user_id, message_text, timestamp, False))
            else:
                cur.execute("""
                    INSERT INTO messages (sender_id, receiver_id, message_text, timestamp, is_deleted)
                    VALUES (?, ?, ?, ?, ?);
                """, (sender_id, user_id, message_text, timestamp, False))

            conn.commit()

        except Exception as e:
            db_close(conn, cur)
            return jsonify({'status': 'error', 'message': str(e)}), 500

    # Получение всех сообщений (GET и POST)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT id, sender_id, message_text, timestamp
            FROM messages
            WHERE ((sender_id = %s AND receiver_id = %s)
               OR (sender_id = %s AND receiver_id = %s))
               AND is_deleted = FALSE
            ORDER BY timestamp;
        """, (sender_id, user_id, user_id, sender_id))
    else:
        cur.execute("""
            SELECT id, sender_id, message_text, timestamp
            FROM messages
            WHERE ((sender_id = ? AND receiver_id = ?)
               OR (sender_id = ? AND receiver_id = ?))
               AND is_deleted = 0
            ORDER BY timestamp;
        """, (sender_id, user_id, user_id, sender_id))

    messages = cur.fetchall()
    db_close(conn, cur)

    # Преобразование сообщений в формат JSON
    messages = [dict(message) for message in messages]

    # Маппинг ID пользователей на имена
    user_names = {
        sender_id: current_user_name,
        user_id: receiver_name
    }

    if request.method == 'POST':
        return jsonify({
            'messages': messages,
            'user_names': user_names,
            'receiver_name': receiver_name,
            'status': 'success'
        })

    return render_template('rgz/chat.html', receiver_id=user_id, current_user_id=sender_id, receiver_name=receiver_name, messages=messages, user_names=user_names)


# Удаление сообщения
@rgz.route('/rgz/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    conn, cur = db_connect()

    try:
        # Проверка, существует ли сообщение
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM messages WHERE id = %s;", (message_id,))
        else:
            cur.execute("SELECT id FROM messages WHERE id = ?;", (message_id,))

        if not cur.fetchone():
            db_close(conn, cur)
            return jsonify({'status': 'error', 'message': 'Сообщение не найдено'}), 404

        # Удаление сообщения
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE messages SET is_deleted = TRUE WHERE id = %s;", (message_id,))
        else:
            cur.execute("UPDATE messages SET is_deleted = 1 WHERE id = ?;", (message_id,))

        conn.commit()
        db_close(conn, cur)

        return jsonify({'status': 'success', 'message': 'Сообщение удалено.'})

    except Exception as e:
        db_close(conn, cur)
        return jsonify({'status': 'error', 'message': str(e)}), 500