STOCK = "TSLA"
COMPANY_NAME = "TESLA"

import requests
from twilio.rest import Client
import os


stock_api_key=os.environ["STOCK_API_KEY"]
stock_api_url="https://www.alphavantage.co/query"

parameters_stock={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK,
    "outputsize":"full",
    "apikey":stock_api_key
}

stock_data=requests.get(stock_api_url,params=parameters_stock)
stock_data.raise_for_status()
all_keys=list(stock_data.json()["Time Series (Daily)"].keys())
today=all_keys[0]
previous_day=all_keys[1]
today_open=stock_data.json()["Time Series (Daily)"][today]["1. open"]
yesterday_close=stock_data.json()["Time Series (Daily)"][previous_day]["4. close"]


percent_change=((float(today_open)-float(yesterday_close))/float(yesterday_close)*100)
percent_change=round(percent_change,2)
sign="⬇️"
if percent_change>0:
    sign="⬆️"
if (percent_change==0.5 or -0.5):
    value="Alert"
else:
    value=""

news_api_key=os.environ["NEWS_API_KEY"]
news_api_endpoint="https://newsapi.org/v2/everything"
new_api_parameters={
    "q":COMPANY_NAME,
    "from":today,
    "sortBy":"Popularity",
    "apikey":news_api_key
}
news=requests.get(news_api_endpoint,params=new_api_parameters)
news.raise_for_status()
news_data=news.json()
news_list=[]
for i in range(3):
        
    news={
        "name":news_data["articles"][i]["source"]["name"],
        "title":news_data["articles"][i]["title"],
        "description":news_data["articles"][i]["description"]
    }
    news_list.append(news)
nt1=news_list[0]["title"]
nt2=news_list[1]["title"]
nt3=news_list[2]["title"]

account_sid=os.environ["ACCOUNT_SID"]
auth_token=os.environ["AUTH_TOKEN"]

client = Client(account_sid, auth_token)
message = client.messages.create(
    body=f"{COMPANY_NAME} stock update\n{value}\n{STOCK}: {percent_change}% {sign}\n\n{nt1}\n\n{nt2}\n\n{nt3}",
    from_="FROM NUMBER",
    to='To NUMBER'
)

print(message.status)

