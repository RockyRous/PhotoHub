import flask
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

import database as db
import psycopg2


# # Создаем приложение Flask
# app = flask.Flask(__name__)
#
# # test
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# @login_manager.user_loader
# def load_user(user_id):
#     # Тут возвращаем данные юзера по его user_id
#     return ''

# Авторизация
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    remember = True if request.form.get('remember') else False

    # Тут нужна проверка email на наличие в бд
    # Если есть, достаем в данные и записываем в переменную user
    user = ['email', 'name', 'password']

    # При неправильном входе
    # flash('Please check your login details and try again.')
    # return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('index'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']

    # Тут нужно сделать проверку на наличие email в бд
    # flash('Email address already exists')
    # return redirect(url_for('signup'))

    # Тут создаем пользователя в базе данных

    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
# Конец Авторизация


@app.route("/")
@login_required
def index():
    # Подключаемся к базе данных
    conn = psycopg2.connect(**db.conn_param)
    cursor = conn.cursor()

    # Получаем все фотографии из таблицы
    cursor.execute(("SELECT * FROM photo"))
    photos = cursor.fetchall()
    cursor.close()

    # Возвращаем шаблон с распакованными данными фотографий
    return render_template("index.html", photos=photos)


@app.route("/add-photo", methods=["POST"])
def add_photo():
    """
    Add a photo to the database
    :return str: Photo added
    """
    # Получаем данные из формы
    title = request.form["title"]
    description = request.form["description"]
    image_path = request.form["image"]

    # Добавляем запись в таблицу
    conn = psycopg2.connect(**db.conn_param)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO photo (author_id, title, description, image_path) VALUES (1, %s, %s, %s)",
        (title, description, image_path),
    )
    conn.commit()

    cursor.close()

    # Возвращаем сообщение об успехе
    return 'Операция произведена'


@app.route("/delete-photo/<id>", methods=["POST"])
def delete_photo():
    """
    delite a photo to the database
    :return str: Photo delite
    """
    # Получаем идентификатор фотографии
    id = request.form["id"]

    # Удаляем запись из таблицы
    conn = psycopg2.connect(**db.conn_param)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM photo WHERE id = %s", (id,))
    conn.commit()

    cursor.close()

    # Возвращаем сообщение об успехе
    return "Фотография удалена!"


@app.route("/edit-photo/", methods=["POST"])
def edit_photo():
    """
    change a photo to the database
    :return str: Photo changed
    """
    # Получаем данные из формы
    title = request.form.get("title")
    image_path = request.form.get("image_path")
    id = request.form["id"]

    # Обновляем запись в базе данных
    conn = psycopg2.connect(**db.conn_param)
    cursor = conn.cursor()

    cursor.execute("UPDATE photo SET title = %s, image_path = %s WHERE id = %s", (title, image_path, id))
    conn.commit()

    cursor.close()

    # Возвращаем сообщение об успехе
    return "Запись обновлена!"


# Запускаем приложение Flask
if __name__ == "__main__":
    app.run(debug=True)