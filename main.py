from flask import render_template, request, redirect, url_for, flash, Flask
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

import database as db
import psycopg2


# Создаем приложение Flask
app = Flask(__name__)
login_manager = LoginManager(app)
# Подключаемся к базе данных
conn = psycopg2.connect(**db.conn_param)


# # Подключаемся к базе данных
# conn = psycopg2.connect(**db.conn_param)
# cursor = conn.cursor()

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
    """ Renders the login page """
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    """ Processing request for login form """
    email = request.form['email']
    password = request.form['password']
    remember = True if request.form.get('remember') else False

    # Check email and password in db
    user = db.get_author_from_db(email, password)
    if user is None:
        # При неправильном входе сообщаем о ошибке
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    else:
        user.pop(0)
        # user = ['email', 'name', 'password'] - было в описании
        # user = ['name', 'email', 'password'] - у меня

        login_user(user, remember=remember)
        return redirect(url_for('index'))


@app.route('/signup')
def signup():
    """ renders the signup page """
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    """ Processing request for signup form """
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']

    if db.is_email_free(email):
        db.add_author(name, email, password)
        return redirect(url_for('login'))
    else:
        flash('Email address already exists')
        return redirect(url_for('signup'))


@app.route('/logout')
@login_required  # Доступ только авторизованым юсерам
def logout():
    """ Logs out the user and redirects to the login page """
    # logout_user()
    return redirect(url_for('index'))
# Конец Авторизация


@app.route("/")

def index():
    # Получаем все фотографии из таблицы
    with conn.cursor() as cursor:
        cursor.execute(("SELECT * FROM photo"))
        photos = cursor.fetchall()

    # Возвращаем шаблон с распакованными данными фотографий
    return render_template("index.html", photos=photos)


@app.route("/add-photo", methods=["POST"])
@login_required
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
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO photo (author_id, title, description, image_path) VALUES (1, %s, %s, %s)",
            (title, description, image_path),
        )
        conn.commit()

    # Возвращаем сообщение об успехе
    return 'Операция произведена'


@app.route("/delete-photo/<id>", methods=["POST"])
@login_required
def delete_photo():
    """
    delite a photo to the database
    :return str: Photo delite
    """
    # Получаем идентификатор фотографии
    id = request.form["id"]

    # Удаляем запись из таблицы
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM photo WHERE id = %s", (id,))
        conn.commit()

    # Возвращаем сообщение об успехе
    return "Фотография удалена!"


@app.route("/edit-photo/", methods=["POST"])
@login_required
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
    with conn.cursor() as cursor:
        cursor.execute("UPDATE photo SET title = %s, image_path = %s WHERE id = %s", (title, image_path, id))
        conn.commit()

    # Возвращаем сообщение об успехе
    return "Запись обновлена!"


# Запускаем приложение Flask
if __name__ == "__main__":
    app.run(debug=True)