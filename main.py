import ssl
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import OrderedDict

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199

cookies = {
    'ASP.NET_SessionId': 'jhrdojjbcdngmavq31rqlf2q',
    'P141uGPDR': 'YES',
    'P141uM': 'NEW',
}

headers = {
    'authority': 'aerod.paperlessfbo.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ASP.NET_SessionId=jhrdojjbcdngmavq31rqlf2q; P141uGPDR=YES; P141uM=NEW',
    'origin': 'https://aerod.paperlessfbo.com',
    'referer': 'https://aerod.paperlessfbo.com/FCMS1.aspx?MSG=1',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

params = {
    'MSG': '1',
}

data = {
    '__LASTFOCUS': '',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': '/wEPDwUKMTYxODY3NTEyNWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgIFDEltYWdlQnV0dG9uMQUNQ2hlY2tSZW1lbWJlchcmWLipfFResyiMILkZnEgD/lTxSfikQD1qWKlYm1wt',
    '__VIEWSTATEGENERATOR': '3134B75E',
    'ScreenWidth': '2160',
    'ScreenHeight': '963',
    'ScreenWidth1': '2560',
    'ScreenHeight1': '1067',
    'PixelRatio': '2',
    'TextError': 'For security reasons your session has expired. Please authenticate again',
    'TextBox1': 'Please Log In',
    'txtUserName': 'ndua',
    'txtPassword': 'chinku564',
    'ButtLogin': 'Log In',
}

def increment_to_time(increment):
    hour = (increment // 2) - 1
    minute = (increment % 2) * 30
    return f'{hour:02d}:{minute:02d}'

##<a href="javascript:__doPostBack('ctl00$ContentPlaceHolder1$GridView2','9$RS=968RC=34')" style="color:Linen;">select</a>
## style="color:Linen;background-color:White;border-color:Gray;border-width:1px;border-style:solid;"
def main():

    df = pd.DataFrame(columns=["plane", "number"])
    plane_dict = OrderedDict()
    plane_dict["plane"] = []
    plane_dict["time"] = []




    # create a session object to persist the login cookies
    session = requests.Session()
    # perform the login request
    response = session.post('https://aerod.paperlessfbo.com/FCMS1.aspx', params=params, cookies=cookies, headers=headers, data=data)

    soup = BeautifulSoup(response.content, "html.parser")

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

    df = pd.DataFrame(plane_dict)
    df = df.sort_values(['plane', 'time'])


    print (df)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
