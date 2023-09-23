import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
# import matplotlib.pyplot as plt
from .psar_func import PSAR
from datetime import datetime ,timedelta
import time
import pytz
from django.conf import settings
import os
from authApp.models import SignalsModal

account_id = "101-002-26702027-001"
access_token = "82eebcc34d68df99a1a598217889dcbc-22af45079e94b01e69a71e23783746b5"

sma_period = 20
wma_period = 20
ist_timezone = pytz.timezone('Asia/Kolkata')

def getSignal(pair,timeframe,sig):
    client = oandapyV20.API(access_token=access_token)

    params = {
        "count": 100,
        "granularity": timeframe
    }
    r = instruments.InstrumentsCandles(instrument=pair, params=params)
    client.request(r)
    data = r.response["candles"]

    price_data = {
        "time": [candle["time"] for candle in data],
        "open": [float(candle["mid"]["o"]) for candle in data],
        "high": [float(candle["mid"]["h"]) for candle in data],
        "low": [float(candle["mid"]["l"]) for candle in data],
        "close": [float(candle["mid"]["c"]) for candle in data]
    }

    df = pd.DataFrame(price_data)
    psarObj = PSAR()
    df['sar'] = df.apply(
    lambda x: psarObj.calcPSAR(x['high'], x['low']), axis=1)

    df["sma"] = df["close"].rolling(window=sma_period).mean()
    weights = list(range(1, wma_period + 1))
    df["wma"] = df["close"].rolling(window=wma_period).apply(lambda prices: sum(weights * prices) / sum(weights), raw=True)

    df['time_IST'] = df.apply(
    lambda x: datetime.strptime(x['time'], "%Y-%m-%dT%H:%M:%S.%f000000Z").replace(tzinfo=pytz.utc).astimezone(ist_timezone).strftime("%H:%M"), axis=1)

    res = confirmationStrategy(df,sig)
    # showGraph(df)
    return res

def confirmationStrategy(df,sig):

    if 'call' in sig['dir']:
        output_time = datetime.strptime(sig['time'], "%H:%M")
        new_time = output_time - timedelta(minutes=5)
        new_time_str = new_time.strftime("%H:%M")
        selected = df[df['time_IST'] == new_time_str]
        if not selected.empty:
            close = selected['close'].item()
            sar = selected['sar'].item()
            wma = selected['wma'].item()
            sma = selected['sma'].item()
            if (close >= sar) and (wma >= sma):
                return True
            else:
                return False
        else:
            return False
    elif 'put' in sig['dir']:
        output_time = datetime.strptime(sig['time'], "%H:%M")
        new_time = output_time - timedelta(minutes=5)
        new_time_str = new_time.strftime("%H:%M")
        selected = df[df['time_IST'] == new_time_str]
        if not selected.empty:
            close = selected['close'].item()
            sar = selected['sar'].item()
            wma = selected['wma'].item()
            sma = selected['sma'].item()
            if (close <= sar) and (wma <= sma):
                return True
            else:
                return False
        else:
            return False


def showGraph(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['time_IST'],df["close"], label="Close Price")
    plt.plot(df['time_IST'],df["sma"], label=f"SMA ({sma_period} days)")
    plt.plot(df['time_IST'],df["wma"], label=f"WMA ({wma_period} days)")
    plt.plot(df['time_IST'],df["sar"],marker="o", label="Parabolic SAR")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Technical Indicators")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def run(instrument,granularity):
    data = SignalsModal.objects.first()
    
    for line in data.signals_text.split("\n"):
        val = line.split(" ")
        t = val[0]
        d = val[1]
        output_time = datetime.strptime(t, "%H:%M")
        alert_time = output_time - timedelta(minutes=5)
        alert_time_str = alert_time.strftime("%H:%M")
        expiry_time = output_time + timedelta(minutes=5)
        expiry_time_str = expiry_time.strftime("%H:%M")
        sig = {
            'time' : t,
            'alert' : alert_time_str,
            "dir" : d.lower()
        }
        current_time = datetime.now(ist_timezone).strftime("%H:%M")
        # print(sig['alert'],current_time)
        if sig['alert'] == current_time:
            res = getSignal(instrument,granularity,sig)
            if res:
                if 'call' in sig['dir']:
                    return("CALL option of EUR/USD at " + sig['time'] + " with 5 min expiry. Set Expiry to " + expiry_time_str)
                elif sig['dir'].lower() == "put":
                    return("PUT option of EUR/USD at " + sig['time'] + " with 5 min expiry. Set Expiry to " + expiry_time_str)                    
    return("Wait for next signal.......")

if __name__ == "__main__":
    instrument = "EUR_USD"
    granularity = "M5"

    while True:
        current_time = datetime.now()
        next_run_time = current_time + timedelta(minutes=5 - (current_time.minute % 5))
        time_to_sleep = (next_run_time.replace(second=0) - current_time).total_seconds()        
        time.sleep(time_to_sleep)
        
        res = run()
        print(res)

    


        


