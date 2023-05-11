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

def app():

    desired_inputs = {}

    desired_inputs["planes"] = os.environ.get('PLANES', 'ALL').split(',') ##List of Type ['12234', '54102']
    desired_inputs["days"] = int(os.environ.get('DAYS', '15'))
    desired_inputs["targeted_date"] = os.environ.get('TARGETED_DATE', 'NONE') ##TODO: ADD
    desired_inputs["duration_hrs"] = int(os.environ.get('DURATION_HRS', '2'))
    desired_inputs["starting_time"] = os.environ.get('STARTING_TIME', '09:00')
    desired_inputs["ending_time"] = os.environ.get('ENDING_TIME', '20:00')
    desired_inputs["send_email"] = os.environ.get('SEND_EMAIL', 'NO')
    desired_inputs["email_address"] = os.environ.get('EMAIL_ADDRESS', 'nikhil9dua@gmail.com')

    #Ref in config.py
    USERNAME = os.environ.get('AEROD_USERNAME')
    PASSWORD = os.environ.get('AEROD_PASSWORD')
    ASP_NET_SessionId = os.environ.get('ASP_NET_SessionId')


    print("***********************")
    print ("SETTINGS:")
    print ("   Planes to find:", desired_inputs["planes"])
    print ("   Lookahead Days:", desired_inputs["days"])
    print ("   Target Dates:",  desired_inputs["targeted_date"])
    print ("   Slot Duration Minimum:", desired_inputs["duration_hrs"])
    print("   Starting Time:", desired_inputs["starting_time"])
    print("   Ending Time:", desired_inputs["ending_time"])
    print("   Send Email?:", desired_inputs["send_email"])
    print("   Email Address:",  desired_inputs["email_address"])
    print("***********************")

    #Initialize Empty DF
    combined_df = pd.DataFrame()

    # Create a session
    session = requests.Session()

    # Login First
    response = session.post('https://aerod.paperlessfbo.com/FCMS1.aspx', params=config.params, cookies=config.cookies,
                            headers=config.headers, data=config.data)

    ####    Make a DF for all weekends in the next X days   ####
    non_weekday_list = make_weekend_list(days_to_find=desired_inputs["days"])
    for date in non_weekday_list:
        print("Making DF for Date", date)
        df = make_base_dataframe(date, desired_inputs)
        if not df.empty:
            df = make_duration_df(df, desired_inputs)
            combined_df = pd.concat([combined_df, df], ignore_index=False)

    print(combined_df)

    if desired_inputs["send_email"] == 'YES':
        send_email(combined_df, email_address=desired_inputs["email_address"])
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

  app()

