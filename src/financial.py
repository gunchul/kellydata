from datetime import date
from dateutil.relativedelta import relativedelta
import yfinance as yf
import matplotlib.pyplot as plt

from env import env_plot_path_get, env_table_path_get
from table import table_gen

finantial_tab = {
    'audusd':["AUDUSD=X","1 AUD to USD"],
    'audkrw':["AUDKRW=X","1 AUD to KRW"],
    'usdaud':["USDAUD=X","1 USD to AUD"],
    'gold':["GLD","GOLD"],
    'voo':["VOO","Vanguard S&P 500 ETF"],
    'dia':["DIA","SPDR Dow Jones ETF"],
}

def finantial_code_get(menu):
    return finantial_tab[menu][0]
def finantial_title_get(menu):
    return finantial_tab[menu][1]

def finantial_data_get(menu, months):
    start_date = date.today() - relativedelta(months=months)
    end_date = date.today()
    df = yf.download(finantial_code_get(menu), start=start_date, end=end_date)
    df = df.sort_index(ascending=False)
    df = df.reset_index()
    return df

def finantial_plot(menu, months, df):
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(df["Date"], df["Close"])
    ax.set(xlabel='Date', ylabel="Rate", title=f"{finantial_title_get(menu)} for {months} months")
    ax.grid()
    fig.savefig(env_plot_path_get(menu, months))
    plt.close()

def finantial_table(menu, month, df):
    df = df.sort_values(by=["Date"], ascending=False)

    headers = ["Date" ,"Price/Rate"]
    rows = []

    for index, row in df.iterrows():
        rows.append([row['date_str'], row['Close']])

    html = table_gen(headers, rows)

    with open(env_table_path_get(menu, month), "w") as f:
        f.write(html)

########################################

def finantial_data_db_to_all():
    menus = ['audusd', 'audkrw', 'usdaud', 'gold', 'voo', 'dia']
    months = [3, 12, 36]
    for menu in menus:
        for month in months:
            df = finantial_data_get(menu, month)
            df['date_str'] = df['Date'].apply(lambda x:x.strftime('%Y-%m-%d'))
            finantial_plot(menu, month, df)
            finantial_table(menu, month, df)

########################################

if __name__ == "__main__":
    finantial_data_db_to_all()
