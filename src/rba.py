import pandas as pd
import datetime

class RBA:
    def __init__(self, db):
        self.db_name = db.db_name_get()
        self.db = db.db_get()

    def data_get(self):
        df = pd.read_html("https://www.rba.gov.au/statistics/cash-rate/")[0]
        df = df.iloc[:-11] # remove last four samples
        return df

    def db_write(self, df):
        for row in df.values:
            try:
                added_date = datetime.datetime.now()
                date = datetime.datetime.strptime(row[0], "%d %b %Y")
                price = row[2]
                changed_rate = row[1]
                mycursor = self.db.cursor()
                sql = f"INSERT INTO {self.db_name}.rba_price(added_date, date, price, changed_rate) VALUES (%s, %s, %s, %s)"
                values = (added_date, date, price, changed_rate)
                mycursor.execute(sql, values)
                self.db.commit()
            except Exception as e:
                print(f"{e}: {date}, {price}, {changed_rate}: ")

    def db_read(self, months = None):
        where = ""
        if months != None:
            where = f"WHERE date >= DATE_SUB(NOW(), INTERVAL {months} MONTH)"
        query = f"SELECT * FROM {self.db_name}.rba_price {where} ORDER by date desc"
        df = pd.read_sql(query, con=self.db)
        return df

if __name__ == "__main__":
    from db import DB
    db = DB()
    rba = RBA(db)

    if False:
        df = rba.data_get()
        rba.db_write(df)
    else:
        df = rba.db_read(36)
        rba.plot(df, "test", "test.png")
