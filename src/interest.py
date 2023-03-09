from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from db import DB
import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time

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
    tables = html.select("table")
    print(tables[2])
    print(f"=========================")
    print(tables[3])


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
            # mycursor = db_conn.cursor()
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
            print(sql)
            print(values)
            # mycursor.execute(sql, values)
            # db_conn.commit()
        except Exception as e:
            print(f"{e}: {sql} {values}")

if __name__ == "__main__":
    interests = {}
    wd = webdriver.Chrome(r"C:\bin\chromedriver_win32_109\chromedriver.exe")
    maps = [
        # ['anz',anz_data_get],
        # ['westpac',westpac_data_get],
        # ['nab',nab_data_get],
        # ['commbank',commbank_data_get],
        ['westpac',westpac_data_get2],
    ]

    for map in maps:
        interests[map[0]] = map[1](wd)
        print(interests[map[0]])

    # interest_insert(interests)
    # print(anz)
    # print(westpac)
    # print(nab)
    # print(commbank)

    wd.quit()
