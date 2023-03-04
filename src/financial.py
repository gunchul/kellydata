from datetime import date
from dateutil.relativedelta import relativedelta
import yfinance as yf
import matplotlib.pyplot as plt

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
    # df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df

def finantial_plot(menu, months, df):
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(df["Date"], df["Close"])
    ax.set(xlabel='Date', ylabel="Rate", title=f"{finantial_title_get(menu)} for {months} months")
    ax.grid()
    fig.savefig(f"C:\\src\\kellydata_php\\images\\{menu}\\{months}.png")

def finantial_table_header():
    return f'''
    <div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
        <tr>
            <th scope="col">Date</th>
            <th scope="col">Price/Rate</th>
        </tr>
        </thead>
        <tbody>
    '''
def finantial_table_tail():
    return '''
        </tbody>
        </table>
    '''
def finantial_table(menu, months, df):
    html = finantial_table_header()
    for index, row in df.iterrows():
        html += f'''
        <tr>
            <td>{row['Date'].strftime('%Y-%m-%d')}</td>
            <td>{row['Close']:.4f}</td>
        </tr>
        '''
    html += finantial_table_tail()

    with open(f"C:\\src\\kellydata_php\\tables\\{menu}\\{months}.html", "w") as f:
        f.write(html)

########################################

def finantial_data_db_to_all():
    menus = ['audusd', 'audkrw', 'usdaud', 'gold', 'voo', 'dia']
    months = [3, 12, 36]
    for menu in menus:
        for month in months:
            df = finantial_data_get(menu, month)
            finantial_plot(menu, month, df)
            finantial_table(menu, month, df)

########################################

if __name__ == "__main__":
    finantial_data_db_to_all()
