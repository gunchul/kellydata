from datetime import date
from dateutil.relativedelta import relativedelta
import yfinance as yf
import matplotlib.pyplot as plt

exchange_tab = {
    'audusd':["AUDUSD=X","1 AUD to USD"],
    'audkrw':["AUDKRW=X","1 AUD to KRW"],
    'usdaud':["USDAUD=X","1 USD to AUD"],
    'gold':["GLD","GOLD"],
    'voo':["VOO","Vanguard S&P 500 ETF"],
    'dia':["DIA","SPDR Dow Jones ETF"],
}

def exchange_code_get(menu):
    return exchange_tab[menu][0]
def exchange_title_get(menu):
    return exchange_tab[menu][1]

############################################################################

class EXCHANGE:
    def __get(self, months):
        start_date = date.today() - relativedelta(months=months)
        end_date = date.today()
        df = yf.download(self.code, start=start_date, end=end_date)
        df = df.sort_index(ascending=False)
        df.reset_index(inplace=True)
        # df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return df

    def __init__(self, menu, month):
        self.menu = menu
        self.month = month
        self.code = exchange_code_get(menu)
        self.title = exchange_title_get(menu)
        self.df = self.__get(month)

    def plot(self):
        fig, ax = plt.subplots()
        fig.set_figwidth(10)
        ax.plot(self.df["Date"], self.df["Close"])
        ax.set(xlabel='Date', ylabel="Rate", title=f"{self.title} for {self.month} months")
        ax.grid()
        fig.savefig(f"C:\\src\\kellydata_php\\images\\{self.menu}\\{self.month}.png")

    def table(self):
        self.df['Date'] = self.df['Date'].dt.strftime('%Y-%m-%d')
        html = f'<div class="table-responsive">\n'
        html += f'<table class="table table-striped table-sm">\n'
        html += f'    <thead>\n'
        html += f'    <tr>\n'
        html += f'        <th scope="col">Date</th>\n'
        html += f'        <th scope="col">Rate</th>\n'
        html += f'    </tr>\n'
        html += f'    </thead>\n'
        html += f'    <tbody>\n'
        for row in self.df.values:
            date = row[0]
            price = row[4]
            html += f'    <tr>\n'
            html += f'        <td>{date}</td>\n'
            html += f'        <td>{price:.4f}</td>\n'
            html += f'    </tr>\n'
        html += f'    </tbody>\n'
        html += f'</table>\n'
        with open(f"C:\\src\\kellydata_php\\tables\\{self.menu}\\{self.month}.html", "w") as f:
            f.write(html)

if __name__ == "__main__":
    menus = ['audusd', 'audkrw', 'usdaud', 'gold', 'voo', 'dia']
    months = [3, 12, 36]
    for menu in menus:
        for month in months:
            exchange = EXCHANGE(menu, month)
            exchange.plot()
            exchange.table()
