import psycopg2
from flask_login import LoginManager

# Данные для подключения к базе данных
conn_param = {
    'dbname': "photohub",
    'user': "postgres",
    'password': "GalaTerror",
    'host': "localhost",
    'port': 5432
}


def init(conn_param: dict) -> None:
    # # Создаем объект подключения
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


# def create_login():
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#
#     @login_manager.user_loader
#     def load_user(user_id):
#         # Тут возвращаем данные юзера по его user_id
#         return ''


if __name__ == '__main__':
    init(conn_param)
    # create_login()
