
from bs4 import BeautifulSoup as soap
import requests
import urllib.request
import pandas as pd

session = requests.session()
username = '2191157204'
password = 'LzZTQzQ0VDQ3TnVZY0twS2gzRWovdz09'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

response = session.get('https://ibank.zenithbank.com/InternetBanking/App/Account/AccountSummary', headers=headers)
cookies = response.cookies
Id = cookies.get_dict()
print(Id)
print("New session created")

page = soap(response.text, 'lxml')
view_state = page.find("input", {'name' : "__VIEWSTATE"})
view_state = view_state["value"]
view_state_gen = page.find("input", {'name' : "__VIEWSTATEGENERATOR"})
view_state_gen = view_state_gen["value"]
event_valid =page.find("input", {'name' : "__EVENTVALIDATION"})
event_valid = event_valid["value"]

data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': view_state,
    '__VIEWSTATEGENERATOR': view_state_gen,
    '__EVENTVALIDATION': event_valid,
    'anotherfakename2': '',
    'ThreatMetrixSession': Id["threatmatrixkey"],
    'ctl00$MainContent$LoginSection$mode$ctrl': 'Password',
    'ctl00_MainContent_LoginSection_mode_ctrl_ClientState': '{"logEntries":[],"value":"2","text":"Password","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}',
    'ctl00$MainContent$LoginSection$UserID$ctrl': username,
    'ctl00$MainContent$LoginSection$Password$ctrl': password,
    'ctl00$MainContent$LoginSection$UserSessionID$ctrl': Id["threatmatrixkey"],
    'ctl00$MainContent$Buttons$Login': 'Login',
}
response = session.post('https://ibank.zenithbank.com/Internetbanking/App/Security/Login', cookies=cookies, headers=headers, data=data)
print("=======login============")
acc_res = session.get('https://ibank.zenithbank.com/Internetbanking/App/Account/AccountSummary')

soup = soap(acc_res.text,'lxml')
table = soup.find('div',{'class':'panel-body'}).find_all('tr')


def data():
    result = getList(table)
    
    """ DataFrame"""
    df = pd.DataFrame(result)
    print(df)
    df.to_csv('demo.csv',index=False,mode='a')


def removing_spaces(text):
    return " ".join(text.split())


def getList(table):
    """ get data list """
    account_data = []
    account_name = []
    balance_data = []
    type_data = []
    available_data = []
    Account_link = []

    for i in table[4:]:
        # column 1 account data 
        account = i.find_all('td')[0].text
        account_data.append(removing_spaces(account))

        # column 2 name data 
        name  = i.find_all('td')[1].text
        account_name.append(removing_spaces(name))


        # column 3 type data 
        type  = i.find_all('td')[2].text
        type_data.append(removing_spaces(type))

        # column 4 balance data 
        balance  = i.find_all('td')[3].text
        balance_data.append(removing_spaces(balance))


        # column 5 available data 
        available  = i.find_all('td')[4].text
        available_data.append(removing_spaces(available))

        # column 6 account href link 
        href = i.find_all('td')[0].find('a').get('href')
        s2 = "Custom"
        href_link = "https://ibank.zenithbank.com/InternetBanking/Custom"+href[href.index(s2) + len(s2):]
        Account_link.append(href_link)

    result = {'Account':account_data, 'Account Name':account_name, 
                'Type':type_data, 'Balance':balance_data , 
                'Available':available_data,'Account Link':Account_link}

    return result



data()