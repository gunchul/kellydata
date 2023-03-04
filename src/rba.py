import pandas as pd
import datetime
from db import DB
import matplotlib.pyplot as plt

def rba_date_to_date(rba_date):
    return datetime.datetime.strptime(rba_date, "%d %b %Y").strftime("%Y-%m-%d")

def rba_data_get():
    df = pd.read_html("https://www.rba.gov.au/statistics/cash-rate/")[0]
    df = df.iloc[:-11] # remove last four samples
    df['date'] = df['Effective Date'].apply(rba_date_to_date)
    return df

def rba_data_db_insert(df):
    db = DB()
    db_name = db.db_name_get()
    db_conn = db.db_get()
    for row in df.values:
        sql = f"""INSERT INTO {db_name}.rba_price(added_date, date, price, changed_rate)
                    VALUES (%s, %s, %s, %s)"""
        values = (datetime.datetime.now(),
                    row[4],
                    row[2],
                    row[1])
        try:
            mycursor = db_conn.cursor()
            mycursor.execute(sql, values)
            db_conn.commit()
        except Exception as e:
            print(f"{e}: {sql} {values}")

def rba_data_db_select(months):
    db = DB()
    db_name = db.db_name_get()
    db_conn = db.db_get()

    query = f"""SELECT *
                FROM {db_name}.rba_price
                WHERE date >= DATE_SUB(NOW(), INTERVAL {months} MONTH)
            """

    df = pd.read_sql(query, con=db_conn)
    return df

def rba_plot(df, months):
    fig, ax = plt.subplots()
    fig.set_figwidth(10)

    ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

    ax.step(df["date"], df["price"], linewidth=2.5, label="rate", where="post")

    last_interest = df.iloc[0]["price"]

    for index, row in df.iterrows():
        diff = row['price'] - last_interest
        if diff < 0:
            color='blue'
        elif diff > 0:
            color='darkred'
        if diff != 0.0:
            plt.text(row['date'], row['price'] + 0.01, row['price'], fontdict={'color':color})
        last_interest = row['price']

    # ax.minorticks_on()

    plt.title(f'RBA Cash Rate Target: Last {months} months')
    plt.savefig(f"C:\\src\\kellydata_php\\images\\rba\\{months}.png")

def rba_table_header():
    return f'''
    <div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
        <tr>
            <th scope="col">Date</th>
            <th scope="col">Rate</th>
            <th scope="col">Changed</th>
        </tr>
        </thead>
        <tbody>
    '''
def rba_table_tail():
    return '''
        </tbody>
        </table>
    '''
def rba_table(df, month):
    df = df.sort_values(by=["date"], ascending=False)

    html = rba_table_header()

    for index, row in df.iterrows():
        html += f'''
        <tr>
            <td>{row['date'].strftime('%Y-%m-%d')}</td>
            <td>{row['price']}</td>
            <td>{row['changed_rate']}</td>
        </tr>
        '''
    html += rba_table_tail()

    with open(f"C:\\src\\kellydata_php\\tables\\rba\\{month}.html", "w") as f:
        f.write(html)

########################################

def rba_data_web_to_db():
    df = rba_data_get()
    rba_data_db_insert(df)

def rba_data_db_to_all():
    months = [3, 12, 36]
    for month in months:
        df = rba_data_db_select(month)
        rba_plot(df, month)
        rba_table(df, month)

########################################

if __name__ == "__main__":
    rba_data_db_to_all()
