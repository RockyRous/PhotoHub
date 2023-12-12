import psycopg2
from flask_login import LoginManager

# Данные для подключения к базе данных
# -- Пока что нет команды на создание базы при ее отсутсвии, но будет --
conn_param = {
    'dbname': "photohub",
    'user': "postgres",
    'password': "GalaTerror",
    'host': "localhost",
    'port': 5432
}


def init(conn_param: dict) -> None:
    """ Создаем таблицу в базе данных проекта """

    # Подключение
    conn = psycopg2.connect(**conn_param)
    cursor = conn.cursor()
    conn.autocommit = True  # устанавливаем авто коммит

    # init (if not exists)
    query = ("""
        -- Создаем таблицу author
        CREATE TABLE IF NOT EXISTS author (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
        );
    
        -- Создаем таблицу photo
        CREATE TABLE IF NOT EXISTS photo (
        id SERIAL PRIMARY KEY,
        author_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        image_path VARCHAR(255) NOT NULL
        );
    """)
    cursor.execute(query)

    # Закрытие
    cursor.close()
    conn.close()


def get_author_from_db(email: str, password: str) -> list[int, str, str, str]:
    """ Connect db and get author \n
    :return list of author or None \n
    ex: (id: int, name: str, emain: str, password: str) """
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_param)

    with conn.cursor() as cursor:
        # запрос
        query = "SELECT * FROM author WHERE email = %s AND password = %s;"

        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        # Если результат не равен None, то email и пароль существуют в базе данных
        if result is not None:
            print(result)
            return result
        else:
            print("Email и пароль не найдены в базе данных")
            return None


def is_email_free(email: str) -> bool:
    """ Is email free? \n
    :return True or False """
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_param)

    with conn.cursor() as cursor:
        # запрос
        query = "SELECT * FROM author WHERE email = %s"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        # Если результат не равен None, то email существуют в базе данных
        if result:
            return False
        else:
            return True


def add_author(name: str, email: str, password: str) -> None:
    """ Adds an author """
    conn = psycopg2.connect(**conn_param)
    with conn.cursor() as cursor:
        query = "INSERT INTO author(name, email, password) VALUES(%s, %s, %s);"
        cursor.execute(query, (name, email, password))
        conn.commit()
        print('New author added')


# def create_login():
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#
#     @login_manager.user_loader
#     def load_user(user_id):
#         # Тут возвращаем данные юзера по его user_id
#         return ''


if __name__ == '__main__':
    # init(conn_param)

    # testing
    # add_author("Popka", "jopka", "123")
    # get_author_from_db('admin@admin.admin', 'admin')
