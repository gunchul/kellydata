from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from db import DB
import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time

from env import env_plot_path_get, env_table_path_get
from table import table_gen

def anz_data_get(wd):
    result = []
    wd.get(f"https://www.anz.com.au/personal/home-loans/offers-and-rates/")
    time.sleep(2)
    html = bs(wd.page_source, "lxml")
    selectors = [
        "#conditionalsection-712277054 > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(2) > p > span",
        "#conditionalsection-712277054 > div:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(2) > p > span",
        "#conditionalsection-712277054 > div:nth-child(2) > table > tbody > tr:nth-child(5) > td:nth-child(2) > p > span",
        "#conditionalsection-1315628067 > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(2) > p > span",
        "#conditionalsection-1315628067 > div:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(2) > p > span",
        "#conditionalsection-1315628067 > div:nth-child(2) > table > tbody > tr:nth-child(5) > td:nth-child(2) > p > span",
    ]
    for selector in selectors:
        result.append(html.select_one(selector).text.split("%")[0])
    return result

def westpac_data_get(wd):
    result = []
    wd.get(f"https://www.westpac.com.au/personal-banking/home-loans/fixed/?cid=wc:hl:WBCHL_1904:sem:sem:sem_westpac%20interest%20rates_e&gclid=Cj0KCQiA0oagBhDHARIsAI-BbgdTGfhFRBy-MpszXnNyEGgJ7nJp5lZbHnU_qFJXRxng7E87bRhutfsaAgP_EALw_wcB&gclsrc=aw.ds")
    time.sleep(2)
    html = bs(wd.page_source, "lxml")
    selectors = [
        "#tabcordian_accordian-collapsible1678276853417 > div.bodycopy > div.table-responsive > table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)",
        "#tabcordian_accordian-collapsible1678276853417 > div.bodycopy > div.table-responsive > table > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(2)",
        "#tabcordian_accordian-collapsible1678276853417 > div.bodycopy > div.table-responsive > table > tbody:nth-child(6) > tr:nth-child(2) > td:nth-child(2)",
        "#tabcordian_accordian-collapsible1678276853429 > div:nth-child(1) > div.table-responsive > table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)",
        "#tabcordian_accordian-collapsible1678276853429 > div:nth-child(1) > div.table-responsive > table > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(2)",
        "#tabcordian_accordian-collapsible1678276853429 > div:nth-child(1) > div.table-responsive > table > tbody:nth-child(6) > tr:nth-child(2) > td:nth-child(2)",
    ]
    for selector in selectors:
        result.append(str(round(float(html.select_one(selector).text.split("%")[0])+0.1, 2)))
    return result

def westpac_data_get2(wd):
    result = []
    wd.get(f"https://www.westpac.com.au/personal-banking/home-loans/fixed/?cid=wc:hl:WBCHL_1904:sem:sem:sem_westpac%20interest%20rates_e&gclid=Cj0KCQiA0oagBhDHARIsAI-BbgdTGfhFRBy-MpszXnNyEGgJ7nJp5lZbHnU_qFJXRxng7E87bRhutfsaAgP_EALw_wcB&gclsrc=aw.ds")
    time.sleep(2)
    html = bs(wd.page_source, "lxml")
    tables = html.find_all("table")

    for table_index in [2,4]: # owner, investor
        for tr_index in [2,5,8]: # 1, 2, 3year
            trs = tables[table_index].find_all("tr")
            td_title = trs[tr_index].find_all("td")[0]
            td_value = trs[tr_index].find_all("td")[1]
            if td_title.text != "With Package# and LVR+ discount":
                raise Exception("Webpage Changed!!!")
            result.append(str(round(float(td_value.text.split("%")[0])+0.1, 2)))
    return result

def nab_data_get(wd):
    result = []

    wd.get("https://www.nab.com.au/personal/interest-rates-fees-and-charges/home-loan-interest-rates")
    time.sleep(2)

    html = bs(wd.page_source, "lxml")
    selectors = [
        "#panel-item_1669729434747 > div > div > div:nth-child(3) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1669729434747 > div > div > div:nth-child(3) > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1669729434747 > div > div > div:nth-child(3) > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1669729485810 > div > div > div:nth-child(3) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1669729485810 > div > div > div:nth-child(3) > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1669729485810 > div > div > div:nth-child(3) > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div:nth-child(2)",
    ]
    for selector in selectors:
        result.append(html.select_one(selector).text.split("%")[0])
    return result

def commbank_data_get(wd):
    result = []

    wd.get(f"https://www.commbank.com.au/home-loans/fixed-rate.html")
    time.sleep(2)

    html = bs(wd.page_source, "lxml")
    selectors = [
        "#rates > div > div:nth-child(1) > div > div > div.table-section > div.table > div:nth-child(3) > div:nth-child(2) > div",
        "#rates > div > div:nth-child(1) > div > div > div.table-section > div.table > div:nth-child(5) > div:nth-child(2) > div",
        "#rates > div > div:nth-child(1) > div > div > div.table-section > div.table > div:nth-child(7) > div:nth-child(2) > div",
        "#rates > div > div:nth-child(2) > div > div > div.table-section > div.table > div:nth-child(3) > div:nth-child(2) > div",
        "#rates > div > div:nth-child(2) > div > div > div.table-section > div.table > div:nth-child(5) > div:nth-child(2) > div",
        "#rates > div > div:nth-child(2) > div > div > div.table-section > div.table > div:nth-child(7) > div:nth-child(2) > div",
    ]
    for selector in selectors:
        result.append(html.select_one(selector).text.split("%")[0])
    return result

def interest_insert(interests):
    db = DB()
    db_name = db.db_name_get()
    db_conn = db.db_get()

    for key in interests.keys():
        try:
            mycursor = db_conn.cursor()
            sql = f"""INSERT INTO {db_name}.interest(added_date, date, bank, fixed_owner_1year_rate, fixed_owner_2year_rate, fixed_owner_3year_rate, fixed_invest_1year_rate, fixed_invest_2year_rate, fixed_invest_3year_rate )
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (datetime.datetime.now(),
                      datetime.datetime.now().strftime("%Y-%m-%d"),
                      key,
                      interests[key][0],
                      interests[key][1],
                      interests[key][2],
                      interests[key][3],
                      interests[key][4],
                      interests[key][5])
            # print(sql)
            # print(values)
            mycursor.execute(sql, values)
            db_conn.commit()
        except Exception as e:
            print(f"{e}: {sql} {values}")

def interest_data_db_select(months):
    db = DB()
    db_name = db.db_name_get()
    db_conn = db.db_get()

    query = f"""SELECT date, bank, fixed_owner_1year_rate, fixed_owner_2year_rate, fixed_owner_3year_rate, fixed_invest_1year_rate,  fixed_invest_2year_rate,  fixed_invest_3year_rate
                FROM {db_name}.interest
                WHERE date >= DATE_SUB(NOW(), INTERVAL {months} MONTH)
                ORDER BY date desc
            """

    df = pd.read_sql(query, con=db_conn)
    return df

def interest_plot(menu, months, df):
    columns = [
        ["fixed_owner_1year_rate", "Fixed Owner 1 Year"],
        ["fixed_owner_2year_rate", "Fixed Owner 2 Year"],
        ["fixed_owner_3year_rate", "Fixed Owner 3 Year"],
        ["fixed_invest_1year_rate", "Fixed Investor 1 Year"],
        ["fixed_invest_2year_rate", "Fixed Investor 2 Year"],
        ["fixed_invest_3year_rate", "Fixed Investor 3 Year"],
    ]

    banks = ["commbank", "nab", "westpac", "anz"]

    df = df.set_index(["date", "bank"])
    df = df.unstack()

    fig, axs = plt.subplots(6, 1)
    fig.set_figwidth(10)
    fig.set_figheight(20)

    for i, col in enumerate(columns):
        for bank in banks:
            axs[i].plot(df.index, df[col[0]][bank], label=bank)
        axs[i].set(xlabel='Date', ylabel="%", title=col[1])
        axs[i].grid()
        axs[i].legend(loc="upper left")

    fig.tight_layout()
    fig.savefig(env_plot_path_get(menu, months))
    plt.close()

def interest_table(menu, month, df):
    headers = ["Date","Bank","Owner 1 Year","Owner 2 Year","Owner 3 Year","Investor 1 Year","Investor 2 Year","Investor 3 Year"]
    rows = []

    for index, row in df.iterrows():
        rows.append([
            f"{row['date_str']}",
            f"{row['bank']}",
            f"{row['fixed_owner_1year_rate']:.2f}",
            f"{row['fixed_owner_2year_rate']:.2f}",
            f"{row['fixed_owner_3year_rate']:.2f}",
            f"{row['fixed_invest_1year_rate']:.2f}",
            f"{row['fixed_invest_2year_rate']:.2f}",
            f"{row['fixed_invest_3year_rate']:.2f}"
        ])

    html = table_gen(headers, rows)

    with open(env_table_path_get(menu, month), "w") as f:
        f.write(html)
######################################################

def interest_data_web_to_db():
    interests = {}
    wd = webdriver.Chrome(r"C:\bin\chromedriver_win32_109\chromedriver.exe")
    maps = [
        ['anz',anz_data_get],
        ['westpac',westpac_data_get2],
        ['nab',nab_data_get],
        ['commbank',commbank_data_get],
    ]

    for map in maps:
        interests[map[0]] = map[1](wd)

    wd.quit()
    interest_insert(interests)

def interest_data_db_to_all():
    months = [3, 12, 36]
    for month in months:
        df = interest_data_db_select(month)
        df['date_str'] = df['date'].apply(lambda x:x.strftime('%Y-%m-%d'))
        interest_plot("interest", month, df)
        interest_table("interest", month, df)

######################################################
if __name__ == "__main__":
    # interest_data_web_to_db()
    interest_data_db_to_all()
