import sqlite3
import os
from datetime import datetime

def createDatabse():

    """
    Create SQLlite database if not exist
    """

    try:

        if(not os.path.isfile('./Database.db')):
            sqliteConnection = sqlite3.connect('Database.db')

            sqlite_create_table_query = '''CREATE TABLE Du3aaData (
                                        id INTEGER PRIMARY KEY,
                                        date TEXT NOT NULL,
                                        time TEXT NOT NULL,
                                        success TEXT NOT NULL,
                                        fail TEXT NOT NULL);'''

            cursor = sqliteConnection.cursor()
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            cursor.close()

    except sqlite3.Error as error:
        print("Failed: ", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def insertData(d, t, s, f):

    """
    Insert data to SQLlite
    """

    try:
        sqliteConnection = sqlite3.connect('Database.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = f"""INSERT INTO Du3aaData
                            (date, time, success, fail)  VALUES  ('{d}', '{t}', '{s}', '{f}')"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()

    except sqlite3.Error as error:
        print("Failed: ", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def readData():

    """
    Read SQLlite table
    """

    try:
        sqliteConnection = sqlite3.connect('Database.db')

        cursor = sqliteConnection.cursor()
        sqlite_select_query = """SELECT * from Du3aaData"""
        cursor.execute(sqlite_select_query)
        output = cursor.fetchall()

        arr = []

        now = datetime.now()
        Date=now.strftime("%F")

        for x in range(len(output)):
            if output[x][1] == str(Date):
                arr.append(output[x])

        print(arr)

    except sqlite3.Error as error:
        print("Failed: ", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()


# createDatabse()
insertData('asd', 'ddd', '333', '32323')
# readData()
