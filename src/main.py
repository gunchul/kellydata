from rba import RBA
from exchange import EXCHANGE
from db import DB
import myplot
import mytable

#########################################################################

def rba_data_get(months):
    db = DB()
    rba = RBA(db)
    return rba.db_read(months)

def rba_plot(df, months):
    myplot.rba_plot(df, f'RBA Cash Rate Target: Last {months} months', f"C:\\src\\kellydata_php\\images\\rba\\{months}.png")

def rba_table(df, months):
    mytable.rba_table(df, f"C:\\src\\kellydata_php\\tables\\rba\\{months}.html")

def rba_all(month):
    df = rba_data_get(month)
    rba_plot(df, month)
    rba_table(df, month)

#########################################################################

def exchange_data_get(months):
    return EXCHANGE().aud_usd_get(months)

def exchange_plot(df, months):
    myplot.exchange_plot(df, f'AUD USD Exchange rate: Last {months} months', f"C:\\src\\kellydata_php\\images\\exchange\\{months}.png")

def exchange_table(df, months):
    mytable.exchange_table(df, f"C:\\src\\kellydata_php\\tables\\exchange\\{months}.html")
#########################################################################

def exchange_all(month):
    df = exchange_data_get(month)
    exchange_plot(df, month)
    exchange_table(df, month)

months = [3,12,36]
for month in months:
    exchange_all(month)
