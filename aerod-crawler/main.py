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

def main_debug():

    df = pd.read_csv('my_data.csv')
    #date = 'Sun 06/18/2023'
    #df = make_base_dataframe(date)

    #df.to_csv('my_data.csv', index=False)

    df = make_duration_df(df)


    print(df)



def main():

    #Create a session
    session = requests.Session()

    #login First
    response = session.post('https://aerod.paperlessfbo.com/FCMS1.aspx', params=config.params, cookies=config.cookies, headers=config.headers, data=config.data)

    combined_df = pd.DataFrame() #empty dataframe
    ##today = datetime.today()
    ##date = today.strftime('%a %m/%d/%Y')

    #df = make_base_dataframe(date)
    #df = make_duration_df(df)

    #combined_df = pd.concat([combined_df, df], ignore_index=False)

    #print(combined_df)


    #####    Make a DF for all weekends in the next 45 days   ####
    non_weekday_list=make_weekend_list(days_to_find=45)
    for date in non_weekday_list:
        print(date)
        df = make_base_dataframe(date)
        df = make_duration_df(df)
        combined_df = pd.concat([combined_df, df], ignore_index=False)


    print(combined_df)
    send_email(combined_df)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   ##df = pd.read_csv('my_data.csv')
   main()
   #main_debug()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
