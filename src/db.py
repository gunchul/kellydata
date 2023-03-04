import mysql.connector
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

if __name__ == "__main__":
    db = DB()
    print(db.db_name_get())
