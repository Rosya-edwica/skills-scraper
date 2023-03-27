from typing import NamedTuple

class CsvProfession(NamedTuple):
    Name:   str
    Level:  int

COLUMN_GROUP = 2
COLUMN_LEVEL = 4
COLUMN_PROFESSION = 6


profession_files = [
    {
        "file": "files/Туризм - Вариации названий.csv",
        "groups": {
                29,
        }
    },
    {
        "file": "files/Автомобилестроение.xlsx - Вариации названий.csv",
        "groups": {
                36,
                9
        }
    },
]


QUERY_CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS profession(
    id SERIAL,
    name TEXT NOT NULL,
    level smallint NOT NULL,
    parsed boolean NOT NULL DEFAULT false,

    PRIMARY KEY(id)
    )"""


QUERY_INSERT_MANY = "INSERT INTO profession(name, level) VALUES(%s, %s)"