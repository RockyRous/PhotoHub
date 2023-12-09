import flask
from flask import render_template
from flask import request
import database as db
import psycopg2


# Создаем приложение Flask
app = flask.Flask(__name__)

# Авторизация
@app.route('/login')
def login():
    return 'Login'


@app.route('/signup')
def signup():
    return 'Signup'


@app.route('/logout')
def logout():
    return 'Logout'
# Конец Авторизация


@app.route("/")
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