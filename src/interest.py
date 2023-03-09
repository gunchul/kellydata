from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from db import DB
import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
from env import PROJECTS

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

    wd.get(f"https://www.nab.com.au/personal/home-loans/nab-fixed-rate-home-loan")
    time.sleep(2)

    html = bs(wd.page_source, "lxml")
    selectors = [
        "#panel-item_1676285757865 > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1676285757865 > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1676285757865 > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1676285819796 > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1676285819796 > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div:nth-child(2)",
        "#panel-item_1676285819796 > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div:nth-child(2)",
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

def interest_plot(df, months):
    banks = ["commbank", "nab", "westpac", "anz"]

    df = df.set_index(["date", "bank"])
    df = df.unstack()

    fig, axs = plt.subplots(6, 1)
    fig.set_figwidth(10)
    fig.set_figheight(20)

    for bank in banks:
        axs[0].plot(df.index, df['fixed_owner_1year_rate'][bank], label=f"{bank}")
        axs[1].plot(df.index, df['fixed_owner_2year_rate'][bank], label=f"{bank}")
        axs[2].plot(df.index, df['fixed_owner_3year_rate'][bank], label=f"{bank}")
        axs[3].plot(df.index, df['fixed_invest_1year_rate'][bank], label=f"{bank}")
        axs[4].plot(df.index, df['fixed_invest_2year_rate'][bank], label=f"{bank}")
        axs[5].plot(df.index, df['fixed_invest_3year_rate'][bank], label=f"{bank}")

    titles = [
                "fixed_owner_1year_rate",
                "fixed_owner_2year_rate",
                "fixed_owner_3year_rate",
                "fixed_investor_1year_rate",
                "fixed_investor_2year_rate",
                "fixed_investor_3year_rate",
             ]
    for i in range(6):
        axs[i].set(xlabel='Date', ylabel="%", title=f"{titles[i]} for {months} months")
        axs[i].grid()
        axs[i].legend()

    fig.tight_layout()
    fig.savefig(PROJECTS["root"] + f"/images/interest/{months}.png")
    plt.close()

def interest_table_header():
    return f'''
    <div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
        <tr>
            <th scope="col">Date</th>
            <th scope="col">Bank</th>
            <th scope="col">Owner 1 Year</th>
            <th scope="col">Owner 2 Year</th>
            <th scope="col">Owner 3 Year</th>
            <th scope="col">Investor 1 Year</th>
            <th scope="col">Investor 2 Year</th>
            <th scope="col">Investor 3 Year</th>
        </tr>
        </thead>
        <tbody>
    '''
def interest_table_tail():
    return '''
        </tbody>
        </table>
    '''
def interest_table(df, months):
    html = interest_table_header()
    for index, row in df.iterrows():
        html += f'''
        <tr>
            <td>{row['date'].strftime('%Y-%m-%d')}</td>
            <td>{row['bank']}</td>
            <td>{row['fixed_owner_1year_rate']:.2f}</td>
            <td>{row['fixed_owner_2year_rate']:.2f}</td>
            <td>{row['fixed_owner_3year_rate']:.2f}</td>
            <td>{row['fixed_invest_1year_rate']:.2f}</td>
            <td>{row['fixed_invest_2year_rate']:.2f}</td>
            <td>{row['fixed_invest_3year_rate']:.2f}</td>
        </tr>
        '''
    html += interest_table_tail()

    with open(PROJECTS["root"] + f"/tables/interest/{months}.html", "w") as f:
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
        interest_plot(df, month)
        interest_table(df, month)

######################################################
if __name__ == "__main__":
    interest_data_db_to_all()
