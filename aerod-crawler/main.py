import ssl
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta
import config
from helpers import *


pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199




def main():

    #Create a session
    session = requests.Session()

    #login First
    response = session.post('https://aerod.paperlessfbo.com/FCMS1.aspx', params=config.params, cookies=config.cookies, headers=config.headers, data=config.data)

    today = datetime.today()
    date = today.strftime('%a %m/%d/%Y')
    make_dataframe(date)
    #Make a DF for all weekends
    # non_weekday_list=make_weekend_list()
    # for date in non_weekday_list:
    #     print(date)
    #     make_dataframe(date)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   #main()
   find_longest_block()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
