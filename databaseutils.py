import mysql.connector
from config import HOST, USER, PASSWORD


class DbExceptionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name,
        port=3306,
    )
    return cnx


def get_all_records():
    db_connection = None
    records = []
    try:
        db_name = 'wema_therapy'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """SELECT * FROM therapy_schedules"""
        cur.execute(query)
        result = cur.fetchall()  # this is a list with db records where each record is a tuple

        for i in result:
            print(i)
            records.append({
                "therapist_name": i[0],
                "dates": i[1],
                "morning_hours": i[2],
                "evening_hours": i[3]
            })
        cur.close()

    except Exception as e:
        print(f"Error: {e}")
        raise DbExceptionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return records


def _map_values(schedule):
    mapped = []
    for item in schedule:
        mapped.append({
            "name": item[0],
            "morning_hours": "Not Available" if item[1] else "Available",
            "evening_hours": "Not Available" if item[2] else "Available"
        })
        print(mapped)
    return mapped


def get_all_booking_availability(_date):
    db_connection = None
    availability = []
    try:
        db_name = "wema_therapy"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to db %s" % db_name)

        query = """
        SELECT therapist_name,morning_hours,evening_hours
        FROM therapy_schedules
        WHERE Dates='{}'
        """.format(_date)

        print(f"Executing query: {query}")
        cur.execute(query)
        result = cur.fetchall()
        print(f"Query result: {result}")

        availability = _map_values(result)
        cur.close()

    except Exception():
        raise DbExceptionError("Failed to read from database")

    finally:
        if db_connection:
            db_connection.close()
            print("Database connection %s closed")

        return availability


def add_booking(_date, therapist_name, time, customer):
    db_connection = None
    try:
        db_name = 'wema_therapy'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB")
        query = """ 
                    UPDATE  therapy_schedules
                   SET `{time}` = 1,
                   `{time_id}`='{customer}'
                   WHERE Dates = '{date}' AND therapist_name='{therapist_name}'
               """.format(time=time, time_id="P_ID" + time, customer=customer, date=_date,
                          therapist_name=therapist_name)


        cur.execute(query)
        db_connection.commit()
        cur.close()

    except Exception:
        raise DbExceptionError("Failed to read from database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection %s closed")

def main():
    # get_all_records()
    get_all_booking_availability('2024-07-02')
    # add_booking()


if __name__ == "__main__":
    main()

#     get_all_booking_availability('2024-07-02')
