import json
import os
import pycron
import requests
import time
from requests.api import head
import yfinance as yf
from datetime import date, datetime
from dotenv import load_dotenv
from pytz import timezone

# Load data from the .env file
load_dotenv()

""" Using ENV file configurations """
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = os.getenv('BASE_URL')

# Printed the variables to confirm the correct values
# print(API_KEY, SECRET_KEY, BASE_URL)

def buy_operation(ticker, qty):
    """ 
    Send a POST request to "/v2/orders" to create a new order
    :param ticker - stock ticker
    :param qty - quantity to buy
    :return - confirmation that the order has been opened
    """
    url = BASE_URL + '/v2/orders'
    payload = json.dumps({
        "symbol": ticker,
        "qty": qty,
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    })

    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': SECRET_KEY,
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, data=payload).json()

def close_position(ticker):
    """ 
    Sends a DELETE request to "/v2/positions" to liquidate an open position
    :param ticker- stock ticker
    :return- confirmation that the position has been closed
    """
    url = BASE_URL + '/v2/positions/' + ticker

    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': SECRET_KEY
    }

    return requests.request("DELETE", url, headers=headers).json()

def get_positions():
    """ 
    Sends a GET request to "/v2/positions" and returns the current positions that are open in our account
    :return - the positions that are held in the Alpaca Trading account
    """
    url = BASE_URL + "/v2/positions"
    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': SECRET_KEY,
    }

    return requests.request("GET", url, headers=headers).json()

def get_moving_averages(ticker):
    """ 
    Calculates the 9 and 30 dats moving average of the specified ticker
    :param ticker - stock ticker
    :return - returns (9 days moving average, 30 days moving average)
    """
    data = yf.download(ticker, period='3mo', interval='1d') #Download the last 3 months worth of data for the ticker

    # Compute a 9-day Simple Moving Average with pandas
    data['SMA_9'] = data['Close'].rolling(window=9, min_periods=1).mean()

    # Compute a 30-day Simple Moving Average with pandas
    data['SMA_30'] = data['Close'].rolling(window=30, min_periods=1).mean() 

    # Get the latest calculated 9 days Simple Moving Average
    SMA_9 = float(data.tail(1)["SMA_9"])  

    # Get the latest 30 days Simple Moving Average
    SMA_30 = float(data.tail(1)["SMA_30"]) 

    return SMA_9, SMA_30


if __name__ == "__main__":
    print("Starting the trading algo")
    while True:
        if pycron.is_now('30 9-15 * * 1-5', dt=datetime.now(timezone('EST'))):
            ticker = "SPY"
            SMA_9, SMA_30 = get_moving_averages(ticker)
            if SMA_9 > SMA_30:
                # We should buy if we don't already own the stock
                if ticker not in [i["symbol"] for i in get_positions()]:
                    print("Currently buying", ticker)
                    buy_operation(ticker, 1)
            if SMA_9 < SMA_30:
                # We should liquidate our position if we own the stock
                if ticker in [i["symbol"] for i in get_positions()]:
                    print("Currently liquidating our", ticker, "position")
                    close_position(ticker)
            # Making sure we don't run the logic twice in a minute
            time.sleep(60)
        else:
            time.sleep(20)  # Check again in 20 seconds
