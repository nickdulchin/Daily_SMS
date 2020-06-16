from twilio.rest import Client
import COVID19Py
import requests
from bs4 import BeautifulSoup
import robin_stocks as r
import config

#covid python api
covid19 = COVID19Py.COVID19(data_source="csbs")
latest = covid19.getLatest()
total_num = latest['confirmed']

#covid nyt
page = requests.get("https://www.nytimes.com/")
soup = BeautifulSoup(page.content, 'html.parser')
#new_nyt = soup.find('h4',{"class":"svelte-pnqaks"}).text

#covid nyt
page = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html")
soup = BeautifulSoup(page.content, 'html.parser')
new = soup.find('span',{"class":"new-cases"}).text[:-11]

#biden
page = requests.get("https://projects.economist.com/us-2020-forecast/president")
soup = BeautifulSoup(page.content, 'html.parser')
pct = soup.find('div',{"class":"table-pct"})
biden = pct.text[-3:]

#robinhood
r.login(username=config.username, password=config.password,expiresIn=2000000)
port = r.profiles.load_portfolio_profile()
p_change = (float(port['equity'])-float(port['adjusted_equity_previous_close']))/float(port['adjusted_equity_previous_close'])*100

# send text with Twilio
client = Client(config.account_sid, config.auth_token)
client.messages.create(to=config.to, 
                       from_=config.from_, 
                       body=f"Daily Changes \nNew US COVD19 cases: {new} \nBiden chance: {biden} \nRobinhood change: {round(p_change,2)}%")
