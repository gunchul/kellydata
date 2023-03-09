from bs4 import BeautifulSoup as bs
from env import PROJECTS
from db import DB
import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt

def corelogic_date_to_date(corelogic_date):
    date_str = " ".join(corelogic_date.split(" ")[2:])
    return datetime.datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")

def auction_data_get():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    response = requests.get("https://www.corelogic.com.au/our-data/auction-results", headers=headers)
    html = bs(response.text, "lxml")
    date = corelogic_date_to_date(html.select_one("#setDate").text)
    table = html.select("table")
    df = pd.read_html(str(table))[0]
    df = df.reset_index()
    df = df.fillna(0)
    return date, df

def auction_data_db_insert(data_date, df):
    db = DB()
    db_name = db.db_name_get()
    db_conn = db.db_get()

    for index, row in df.iterrows():
        if row['City'] == "Combined Capitals*":
            continue
        try:
            mycursor = db_conn.cursor()
            sql = f"""INSERT INTO {db_name}.auction(added_date, date, city, total_auctions, sold_prior_to_auction, sold_at_auction, sold_after_auction, passed_in, withdrawn, clearance_rate, cleared_auctions, uncleared_auctions)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (datetime.datetime.now(),
                        data_date,
                        row['City'],
                        row['Total auctions'],
                        row['Sold prior to auction'],
                        row['Sold at auction'],
                        row['Sold after auction'],
                        row['Passed in'],
                        row['Withdrawn'],
                        float(row['Clearance rate'].rstrip("%")) / 100,
                        row['Cleared Auctions'],
                        row['Uncleared Auctions'])
            mycursor.execute(sql, values)
            db_conn.commit()
        except Exception as e:
            print(f"{e}: {sql} {values}")

def auction_data_db_select(months):
    db = DB()
    db_name = db.db_name_get()
    db_conn = db.db_get()

    where = f"WHERE date >= DATE_SUB(NOW(), INTERVAL {months} MONTH)"

    query = f"""SELECT date, city, total_auctions, clearance_rate
                FROM {db_name}.auction
                {where}
                ORDER by date desc"""
    df = pd.read_sql(query, con=db_conn)
    return df

def auction_plot(df, months):
    cities = ["Brisbane", "Melbourne", "Sydney"]

    df = df.set_index(["date", "city"])
    df = df.unstack()
    df['clearance_rate'] = df['clearance_rate'] * 100

    fig, axs = plt.subplots(2, 1)
    fig.set_figwidth(10)

    for city in cities:
        axs[0].plot(df.index, df['clearance_rate'][city], label=f"{city}")
        axs[1].plot(df.index, df['total_auctions'][city], label=f"{city}")

    axs[0].set(xlabel='Date', ylabel="Percent(%)", title=f"Clearance Rate(%) for {months} months")
    axs[0].grid()
    axs[0].legend()
    axs[1].set(xlabel='Date', ylabel="Count", title=f"Total Auctions for {months} months")
    axs[1].grid()
    axs[1].legend()

    fig.tight_layout()
    fig.savefig(PROJECTS["root"] + f"/images/auction/{months}.png")

def auction_table_header():
    return f'''
    <div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
        <tr>
            <th scope="col">Date</th>
            <th scope="col">City</th>
            <th scope="col">Total Auctions</th>
            <th scope="col">Clearance Rate(%)</th>
        </tr>
        </thead>
        <tbody>
    '''
def auction_table_tail():
    return '''
        </tbody>
        </table>
    '''
def auction_table(df, month):
    cities = ["Brisbane", "Melbourne", "Sydney"]
    df['clearance_rate'] = df['clearance_rate'] * 100

    html = auction_table_header()

    for index, row in df.iterrows():
        html += f'''
        <tr>
            <td>{row['date'].strftime('%Y-%m-%d')}</td>
            <td>{row['city']}</td>
            <td>{row['total_auctions']}</td>
            <td>{row['clearance_rate']:.2f}</td>
        </tr>
        '''
    html += auction_table_tail()

    with open(PROJECTS["root"] + f"/tables/auction/{month}.html", "w") as f:
        f.write(html)

########################################

def auction_data_web_to_db():
    data_date, df = auction_data_get()
    auction_data_db_insert(data_date, df)

def auction_data_db_to_all():
    months = [3, 12, 36]
    for month in months:
        df = auction_data_db_select(month)
        auction_plot(df, month)
        auction_table(df, month)

########################################

if __name__ == "__main__":
    # auction_data_web_to_db()
    auction_data_db_to_all()
