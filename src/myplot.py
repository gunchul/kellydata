import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta

def rba_plot(df, title, output_path):
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
    plt.title(title)
    plt.savefig(output_path)

def exchange_plot(df, title, output_path):
    fig, ax = plt.subplots()

    fig.set_figwidth(10)

    ax.plot(df["Date"], df["Close"])
    ax.set(xlabel='Date', ylabel="1 AUD to USD", title=title)
    ax.grid()

    fig.savefig(output_path)

if __name__ == "__main__":
    df = pd.read_csv(r"C:\src\kellydata\tmp\rba.csv")
    rba_plot(df, f'RBA Cash Rate Target', r"C:\src\kellydata\tmp\tmp.png")
