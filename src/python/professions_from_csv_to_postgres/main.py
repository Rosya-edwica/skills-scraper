from config import profession_files
from csv_file import get_professions_from_csv
from postgres import move_professions_to_postgres


def main():
    for prof_area in profession_files:
        professions = get_professions_from_csv(csv_file=prof_area["file"], groups=prof_area["groups"])
        move_professions_to_postgres(professions)

        break


if __name__ == "__main__":
    main()
