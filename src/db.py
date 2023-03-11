import mysql.connector
from mysql.connector import errorcode
from env import DATABASE

class DB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = DATABASE["host"],
            user = DATABASE["user"],
            password = DATABASE["password"],
            database = DATABASE["database"])

    def __del__(self):
        self.db.close()

    def db_get(self):
        return self.db

    def db_name_get(self):
        return DATABASE["database"]

    def insert(self, sql, values):
        try:
            mycursor = self.db.cursor()
            mycursor.execute(sql, values)
            self.db.commit()
        except mysql.connector.Error as err:
            if err.errno != errorcode.ER_DUP_ENTRY:
                print(f"ERROR: {err}: {sql} {values}")
                raise err

if __name__ == "__main__":
    db = DB()
    print(db.db_name_get())
