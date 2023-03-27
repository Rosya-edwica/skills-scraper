import csv
from config import *


def get_professions_from_csv(csv_file: str = "Туризм - Вариации названий.csv", groups: list[int] = []) -> list[CsvProfession]:
    professions: list[CsvProfession] = []
    
    with open(csv_file, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for index, row in enumerate(reader):
            if index == 0 or int(row[COLUMN_GROUP]) not in groups: continue
            professions.append(CsvProfession(
                Name=row[COLUMN_PROFESSION].replace("\n", ""),
                Level=int(row[COLUMN_LEVEL])
            ))
    return professions

