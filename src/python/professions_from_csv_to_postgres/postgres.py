import psycopg2

from config import CsvProfession, QUERY_CREATE_TABLE, QUERY_INSERT_MANY


def connect_to_postgres() -> psycopg2.extensions.connection:
    try:
        connect = psycopg2.connect(database="edwica", user="postgres", host="127.0.0.1", port="5432", password="admin")
        return connect
    except BaseException as err:
        exit(err)

def create_table_if_not_exist():
    connect = connect_to_postgres()
    cursor = connect.cursor()
    try:
        cursor.execute(QUERY_CREATE_TABLE)
        connect.commit()
    except BaseException as err:
        exit(err)
    finally:
        connect.close()


def move_professions_to_postgres(data: list[CsvProfession]):
    create_table_if_not_exist()
    connect = connect_to_postgres()
    cursor = connect.cursor()
    try:
        cursor.executemany(QUERY_INSERT_MANY, ((i.Name, i.Level) for i in data))
        connect.commit()
    except BaseException as err:
        exit(err)
    finally:
        connect.close()

