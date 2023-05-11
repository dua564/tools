import os

cookies = {
    'ASP.NET_SessionId': os.environ.get('ASP_NET_SessionId'),
    'P141uGPDR': 'YES',
    'P141uM': 'NEW',
}

headers = {
    'authority': 'aerod.paperlessfbo.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
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
    'txtUserName': os.environ.get('AEROD_USERNAME'),
    'txtPassword': os.environ.get('AEROD_PASSWORD'),
    'ButtLogin': 'Log In',
}
