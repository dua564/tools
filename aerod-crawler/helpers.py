import ssl
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta
import config

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
        '__VSTATE': 'H4sIAAAAAAAEAO2YXXfbthnHRViwnFiy6Nhh0qRz2SZd41iKCeiFVM52zmK7tpP4bZbrnl35wCQksaZIl6TUalf9PvtI+yi9aB8AguV2S9Kb7SpyAD7A/yEI/Eg8APKLUX1YxGsXF9tJnKdJlJ3y70dhyk+SLN9i/tVbPrm4sEq46ueR4zy9HOVR0k96PbyuKsRtPM5PIubz/SQKeEqeXuZx1x/w4CTl4x02wc8+7HrEfxSeT9/tuT24Oo75Cetz/OV7vQ4Sn+VhEuPn73Pj/lV3kPzQzVkcXE7e73t1yofJmO+GUc7TDK+92zfoj0m1H+An73bZS8PgPOQ//FE/Wv3LRqFsLCAjqOI7ntPyiNsm7aqF1lbOWRQGLOfinfEsP0wCjgwL9aqBVUQG5AhycCwOUg5vbJDn19nLzU3G0yR4cc2ueRrxLOtdJi/8ZLh5fR35WfYCUoDm4OZ76EFV3F06D7PwMuKDIECfiJrPkDA3ZmZ9ZrozszMz/yobKp7xH3O8uDNiNfsovBqEEUivpNccrpLWy0bH/uZs26YULJC+hk4s9JTOoWyAWVyb3+dhf5A/LojfT9//zYDLWvHi8+4W+skIrIdqyHg7YlmGi1tJMLHmBZElGJQZVC2jZxnmb3qBMaFN2u6DFKDStD8Lrc3WJnVoAx5cgRvN+5VCmVDaaNrPiEsP18vUdRu7UPDoGyh4De/vUjlYrzTbTvNcFk731sutJnGoLJ2sl+HVNdxpCxUodHdv/Npup72vG+841J0V2t7ptm6h4zW91rQwv3d6/M3RDnQNy65h2ScsO4NlL7B8OpaPxfJ5WD4Hywdg2TKWTU7bWt2Yq/Rv/ySV5f9C5YGkYha7xwfHlS0+iHhcs9/yOJ7cgfkVC7qpuZ1EURhnNXsrZUHEJws7Sc0+G7Ckus/SyyEDt72UDdjwEXz4EUzGmv2G93opn9j1etdP8rxeX9ofBVkCngeT+J8hX3rLcsbHNbvL0z6fLJ7AXIY2JxFPy90wGsN7PRj5LDPF5E6+4+PQr9mvxywud0fQyLch9IgNV89h6kT1IwZTJ6/ZhyGEoWjxW5bLJ73hcXXqCH2X/bhvGg5QbjRbkHtNCnmr5WJCGs0G2PCHieO125C3vSbUO57w8TpQQ2HKCk8iWnAbsr7pgacjPB3itgC72f/dT5J/LD9ap4cMhNAcKiKM5lEJLaA76C5aRGVUQUuoiky0jO6hFbSK7iMLPUAP0SfoEXqMPkV/QmswC230OfoCPUFP0Zfoz+gr9Ayto+doA9VQHb1Am5ZjYuw4Lx1neumrcsOZXmSZKJ1onSidaJ0qnWqdKp1qvaH0htYbSm9ovan0ptabSm9qvaX0ltZbSm9pva30ttbbSm9r3VW6q3VX6a7WPaV7WveU7mm9o/SO1jtK70x1ovgRzY8ofkTzI4of0fyI4kc0P6L4Ec2PKH5E8yOKH9H8iOJHND+i+BHNjyh+RPMjih/R/IjiRzQ/ovgRzY8ofkTzI4of0fyI4kc0P6L4Ec2PKH5E8yOKH9H8iOJHND+q+FHNjyp+VPOjih/V/KjiRzU/qvhRzY8qflTzo4of1fyo4icvMNmQHaDP5GwzPzDbLNPE87uRWIawIZqa30uTURxgg0ChcnR8Zr8aszBisGpig0KdeZKGY1ip7bOUhXEY97HRgOqV13GWp6MhLP63lKZQtpPhkKd+yKJbSmt2j58n6S2lDcrS4SjKw1uVLlRWt0ZZGMMyb+sOe6I/O2Hmw54mndxUd6D6jtwYnYYBx4iIgZW2ByyFXQ8UxdAed/kwjFlaO+Q8h0fUugx2EPbXYxgAuIiRrr4KUz9lvdw+hG7AtobFvmhNDHdRNs8D+3gk3MU47+qq1zHUtFTM01uXj5HvY+T7GPn+D5HviwAhPefkpr0fwA82zDc7eDwVwLYKepdcgENJgBZnXpXfet2XxbXSdI6rRp/M3L+amesz8/nMrInDz12jIFpB3R3LmC8Usn/9fPDvhWDW40CdeO71lCXytVIS+1HoX+FH37Exy/w0vM5f+hFn6Vk45Mkof5avq1MOkscKsbct76ahfWt/O6/aE0Fo5Q8FIWvFxAg4IwkZOUQkaVGRpNUQSVpNkaTVEklabZGk5YokLU8kaXVEEhZsI1V4hqg8jcwQfKcBGELtNNxChJ1GWYisMroKqy2StFyRpOWJpM8/atSCSUm9sYX/rKpMWesXtXTLBSrgnDYlZhXhc6u/OjioTy96tbwm+iqWGWnBmV0bN15UX1XvzNk7wTfvxMImNp7DP7ir+Pbw9B8ql6XT/XOVy1L3qKtyKM3ll4HMxARA4ohz0/TyB1+3tQwrnfgPBHsbVvV+AusonHSSNMOoLgb0cXfwP9kdwJd2V390MHNLIjwsI8O0CuKvvLpRKAS/ApFGB/HSEgAA',
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

def make_weekend_list():
    today = datetime.today()
    date = today.strftime('%a %m/%d/%Y')

    # Define a timedelta object with a value of one day
    delta = timedelta(days=1)

    # Create a list to store the dates
    date_list = []

    # Loop through the next 45 days
    for i in range(45):
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


def make_dataframe(date):
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

    print("Current Date is: ", date)

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
                plane_dict["plane"].append(plane)
                plane_dict["time"].append(time)
                plane_dict["date"].append(date)

    df = pd.DataFrame(plane_dict)
    df = df.sort_values(['plane', 'time'])

    df = find_longest_block(df)
    print (df)


def find_longest_block(df):
    df['time'] = pd.to_datetime(df['time'])

    earliest_time = df.groupby('plane')['time'].min()
    latest_time = df.groupby('plane')['time'].max()

    time_diff = latest_time - earliest_time

    df = pd.DataFrame({
        'earliest_time': earliest_time,
        'latest_time': latest_time,
        'time_diff': time_diff
    })

    df['time_diff'] = df['time_diff'] + pd.Timedelta(minutes=30)

    df['earliest_time'] = df['earliest_time'].dt.strftime('%H:%M')
    df['latest_time'] = df['latest_time'].dt.strftime('%H:%M')
    df['time_diff'] = df['time_diff'].apply(
        lambda x: '{:02d}:{:02d}'.format(int(x.seconds / 3600), int((x.seconds / 60) % 60)))

    return df
