import ssl
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta
import config
import click
import os
from click.testing import CliRunner
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

@click.command()
@click.option('--planes', '-p', multiple=True, help="Comma separated list of planes (eg:-p 12234,61637")
@click.option('--days', '-d', default=45, show_default=True, help="Future days to find")
def cli_app(planes, days):

    plane_tuple = planes
    print(plane_tuple)
    click.echo(','.join(planes))
    click.secho("Days:{}".format(days), fg='blue')

def app():
    planes = os.environ.get('PLANES', '12234,54102').split(',')
    days = int(os.environ.get('DAYS', '15'))
    duration_hrs = int(os.environ.get('DURATION_HRS', '3'))

    print("**********")
    print ("SETTINGS:")
    print ("   Planes to find:", planes)
    print ("   Lookahead Days:", days)
    print ("   Slot Duration Minimum:", duration_hrs)
    print("**********")



    #Initialize Empty DF
    combined_df = pd.DataFrame()

    # Create a session
    session = requests.Session()

    # Login First
    response = session.post('https://aerod.paperlessfbo.com/FCMS1.aspx', params=config.params, cookies=config.cookies,
                            headers=config.headers, data=config.data)

    ####    Make a DF for all weekends in the next 45 days   ####
    non_weekday_list = make_weekend_list(days_to_find=days)
    for date in non_weekday_list:
        print("Making DF for Date", date)
        df = make_base_dataframe(date)
        df = make_duration_df(df)
        combined_df = pd.concat([combined_df, df], ignore_index=False)

    ## Filter DF Based on Conditions
    if 'ALL' in planes:
        df_filtered = combined_df
    else:
        df_filtered = combined_df[combined_df['plane'].isin(planes)]

    print(df_filtered)
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

  app()
  #runner = CliRunner()
  #result = runner.invoke(cli_app, ['--message', 'test'])
   #pass

   #cli_app()
   ##df = pd.read_csv('my_data.csv')
   ##main()
   #main_debug()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
