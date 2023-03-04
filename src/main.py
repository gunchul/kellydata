from auction import auction_data_web_to_db
from auction import auction_data_db_to_all
from financial import finantial_data_db_to_all
from rba import rba_data_web_to_db
from rba import rba_data_db_to_all

def data_get():
    auction_data_web_to_db()
    rba_data_web_to_db()

def data_gen():
    auction_data_db_to_all()
    rba_data_db_to_all()
    finantial_data_db_to_all()


data_get()
data_gen()
