import ssl
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta
import config
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

###############     HELPERS   ################################

def increment_to_time(increment):
    hour = (increment // 2) - 1
    minute = (increment % 2) * 30
    return f'{hour:02d}:{minute:02d}'
def change_date(date):

    data = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$DropDate1',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VSTATE': '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',
        '__VIEWSTATE': '',
        '__PREVIOUSPAGE': 'v-bHinyS8OjUmZ4HoDkupaSuF0LtqS93ahDQWaAUM6qPn1QULz2hcEVWG8SJ8aXFTzRpUME8OaYiKwV8t7b1Lz0cFAAph981rXuIEgxPhh01',
        'ctl00$ContentPlaceHolder1$DropDate1': date,
        'ctl00$ContentPlaceHolder1$DropTime': '00',
        'ctl00$ContentPlaceHolder1$ChkOnePage': 'on',
        'ctl00$ContentPlaceHolder1$ChkLocation': 'on',
        'ctl00$ContentPlaceHolder1$DDLlocation': 'KRHV',
        'ctl00$ContentPlaceHolder1$DDLShowCats': '-1',
        'Copyright': '© Paperless141, LLC-2003-2023-, a Montana, USA Company',
    }

    return data

def make_weekend_list(days_to_find=45):
    today = datetime.today()
    date = today.strftime('%a %m/%d/%Y')

    # Define a timedelta object with a value of one day
    delta = timedelta(days=1)

    # Create a list to store the dates
    date_list = []

    # Loop through the next 45 days
    for i in range(days_to_find):
        # Add the current date to the list
        date_list.append(today.strftime('%a %m/%d/%Y'))
        # Increment the date by one day
        today += delta

    # Create an empty list to store the non-weekday dates
    non_weekday_list = []

    # Loop through the dates
    for date_str in date_list:
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%a %m/%d/%Y')
        # Check if the date is not a weekday (i.e., a weekend)
        if date.weekday() >= 5:
            # Add the date string to the non-weekday list
            non_weekday_list.append(date_str)

    return non_weekday_list

def check_in_filter(plane, time, desired_inputs):

    is_plane_good = False
    is_time_good = False

    ## Check if plane of interest is good and within desired inputs for planes
    if plane in desired_inputs["planes"] or "ALL" in desired_inputs["planes"]:
        #print("Good Plane: ", plane)
        is_plane_good = True
    else:
        #print("Bad Plane: ", plane)
        is_plane_good = False

    time_obj = datetime.strptime(time, '%H:%M').time()
    start_time_obj = datetime.strptime(desired_inputs["starting_time"], '%H:%M').time()
    end_time_obj = datetime.strptime(desired_inputs["ending_time"], '%H:%M').time()

    ## Check if time is good and within desired inputs for time
    if start_time_obj <= time_obj < end_time_obj:
       # print(time + " is between " + desired_inputs["starting_time"]
       #       + " and " + desired_inputs["ending_time"])
       is_time_good = True
    else:
        # print(time + " is not between " + desired_inputs["starting_time"]
        #      + " and " + desired_inputs["ending_time"])
        is_time_good = False
    if is_plane_good and is_time_good:
        return True

def drop_durations(longest_blocks, duration, desired_inputs):

    new_duration_list = []
    new_longest_block = []


    for dur, block in zip(duration, longest_blocks):
        #print(dur, block)
        if dur >= desired_inputs["duration_hrs"]:
            new_duration_list.append(dur)
            new_longest_block.append(block)

    return new_longest_block, new_duration_list

def make_base_dataframe(date, desired_inputs):
    df = pd.DataFrame(columns=["plane", "number"])
    plane_dict = OrderedDict()
    plane_dict["plane"] = []
    plane_dict["time"] = []
    plane_dict["date"] = []

    data_with_date = change_date(date)
    response = requests.post('https://aerod.paperlessfbo.com/mstr7.aspx', cookies=config.cookies,
                             headers=config.headers, data=data_with_date)

    soup = BeautifulSoup(response.content, "html.parser")

    input_tag = soup.find('input', {'id': 'ctl00_ContentPlaceHolder1_DropDate1'})
    date = input_tag['value']

    #print("Current Date is: ", date)

    # Find all <td> tags that have a style attribute
    td_tags = soup.find_all("td", attrs={
        "style": "color:Linen;background-color:White;border-color:Gray;border-width:1px;border-style:solid;"})

    # Iterate over the matching <td> tags and print the contents of <a> tags inside them
    for td in td_tags:
        links = td.find_all("a")
        for link in links:
            javascript = link.attrs["href"]
            match = re.search(r'RS=([a-zA-Z0-9]+)=(\d+)', javascript)
            if match:
                plane = match.group(1)
                number = match.group(2)
                time = increment_to_time(int(number))
                if(check_in_filter(plane, time, desired_inputs)):
                    plane_dict["plane"].append(plane)
                    plane_dict["time"].append(time)
                    plane_dict["date"].append(date)

    df = pd.DataFrame(plane_dict)
    df = df.sort_values(['plane', 'time'])


    return df


def make_duration_df(df, desired_inputs):

    plane_dict = df.groupby('plane').apply(lambda x: x[['time', 'date']].to_dict(orient='list')).to_dict()
    duration_dict = {}

    for key, value in plane_dict.items():
        plane = key
        date = value['date'][0]
        times = value['time']
        longest_blocks, duration = find_longest_block(times)
        longest_blocks, duration = drop_durations(longest_blocks, duration, desired_inputs)

        if len(longest_blocks) > 0 and len (duration) > 0: #Drop if empty
            duration_dict[plane] = {'blocks': longest_blocks, 'duration': duration, 'date': date}

    # dictionary to dataframe
    df = pd.DataFrame([(k, v['blocks'], v['duration'], v['date']) for k, v in duration_dict.items()],
                      columns=['plane', 'blocks', 'duration', 'date'])


    return df



def find_longest_block(times):

    # convert strings to datetime objects
    times = [datetime.strptime(t, '%H:%M') for t in times]

    consecutive_times = []
    start_time = end_time = None
    for i in range(len(times)):
        if i == 0 or times[i - 1] != times[i] - timedelta(minutes=30):
            start_time = times[i]
        end_time = times[i]
        if i == len(times) - 1 or times[i + 1] != times[i] + timedelta(minutes=30):
            consecutive_times.append((start_time, end_time))
            start_time = end_time = None

    consecutive_times_str = []
    for start_time, end_time in consecutive_times:
        start_time_str = start_time.strftime('%H:%M')
        end_time_str = end_time.strftime('%H:%M')
        consecutive_times_str.append((start_time_str, end_time_str))

    durations = []
    for start, end in consecutive_times_str:
        duration = datetime.strptime(end, '%H:%M') - datetime.strptime(start, '%H:%M')
        durations.append(duration)

    hours = []

    durations_list = [str(duration) for duration in durations]

    for duration in durations_list:
        h, m, s = map(int, duration.split(':'))
        duration_in_seconds = timedelta(hours=h, minutes=m, seconds=s).total_seconds()
        duration_in_hours = duration_in_seconds / 3600
        hours.append(duration_in_hours)
    hours_with_half = [h + 0.5 for h in hours]
    ##hours_with_suffix= [f"{h}h" for h in hours_with_half]
    return(consecutive_times_str, hours_with_half)






def send_email(df, email_address):


    table_html = '<html><body>' + df.to_html() + '</body></html>'

    # Set up email parameters
    sender_email = 'nikhil9duapython@gmail.com'
    sender_password = 'qprzjxfftpcjyfrf'
    receiver_email = email_address
    subject = 'Aerod Crawler - Notification'

    # Create the email message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add the html table to the message
    html_part = MIMEText(table_html, 'html')
    msg.attach(html_part)

    # Connect to SMTP server and send the email
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
    smtp_server.quit()
