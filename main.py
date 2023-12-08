import flask
from flask import render_template
from flask import request
import database as db
import psycopg2


# Создаем приложение Flask
app = flask.Flask(__name__)


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
    # Получаем данные из формы
    title = request.form["title"]
    description = request.form["description"]
    image_path = request.form["image"]

    # Добавляем запись в таблицу
    conn = psycopg2.connect(**db.conn_param)
    cursor = conn.cursor()
    print('connect successful')
    cursor.execute(
        "INSERT INTO photo (author_id, title, description, image_path) VALUES (1, %s, %s, %s)",
        (title, description, image_path),
    )
    print('insert successful')
    conn.commit()
    print('commit successful')

    # Возвращаем сообщение об успехе
    return 'Операция произведена'


@app.route("/delete-photo/<id>", methods=["POST"])
def delete_photo(id):
    # Получаем идентификатор фотографии
    id = request.form["id"]
    print('open delete_photo')
    # Удаляем запись из таблицы
    conn = psycopg2.connect(**db.conn_param)
    cursor = conn.cursor()
    print('connect successful')
    cursor.execute("DELETE FROM photo WHERE id = %s", (id,))
    print('delete successful')
    conn.commit()
    print('commit successful')

    # Возвращаем сообщение об успехе
    return "Фотография удалена!"


# Запускаем приложение Flask
if __name__ == "__main__":
    app.run(debug=True)