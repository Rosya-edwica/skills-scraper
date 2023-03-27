import pymysql

from rabota_ru_cities.config import SETTINGS, Region


def connect_to_mysql():
    try:
        connect = pymysql.connect(
            host=SETTINGS.Host,
            port=int(SETTINGS.Port),
            database=SETTINGS.Database,
            user=SETTINGS.User,
            password=SETTINGS.Password,
        )
        return connect
    except BaseException as err:
        exit(err)
    

def update_mysql_city_table(regions: list[Region]):
    connect = connect_to_mysql()
    with connect.cursor() as cursor:
        for region in regions:
            try:
                query = f"""UPDATE h_city
                SET id_rabota_ru='{region.Id}'
                WHERE LOWER(name)='{region.Name.lower()}'"""
                cursor.execute(query)
                print("Success for ", region.Name)
            except BaseException as err:
                exit(err)
            
    connect.commit()
    connect.close()