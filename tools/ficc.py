import yfinance as yf
import fredapi as fa
import configparser
import os
import sys
import datetime
import time
from tqdm import tqdm

account                     = configparser.RawConfigParser()
account.read('config.ini')

try:
    fredapikey              = account['api']['fred']
except KeyError:
    os.system("cls" if os.name == "nt" else "clear")
    print("Run setup.py first")
    sys.exit(1)

ficc_symbol                  = {
                                "US02Y"         : "DGS2",
                                "US10Y"         : "DGS10",
                                "US10Y-2YS"     : "T10Y2Y",
                                "DXY"           : "DX-Y.NYB",
                                "USD/EUR"       : "EUR=X",
                                "USD/CNY"       : "CNY=X",
                                "USD/JPY"       : "JPY=X",
                                "USD/KRW"       : "KRW=X",
                                "Crude Oil"     : "CL=F",
                                "Gold"          : "GC=F",
                                "Cooper"        : "HG=F",
                                "Corn"          : "ZC=F",
                                "Wheat"         : "ZW=F"
                            }
def us_yield(ticker:str, max_retries=3, wait_time=5) -> tuple:
    for retry in range(max_retries):
        try:
            fred            = fa.Fred(api_key=fredapikey)
            daily           = fred.get_series(ticker, limit=21, sort_order="desc").dropna()
            daily_chg       = fred.get_series(ticker, units="pch", limit=2, sort_order="desc").dropna().iloc[0]
            weekly          = fred.get_series(ticker, frequency="w", aggregation_method="eop", limit=3, sort_order="desc").dropna()
            monthly         = fred.get_series(ticker, frequency="m", aggregation_method='eop', observation_start=f"{datetime.datetime.now().year-1}-12-01", sort_order='desc').dropna()
            yearly          = fred.get_series(ticker, frequency="a", aggregation_method='eop', observation_start=f"{datetime.datetime.now().year-1}-12-01", sort_order='desc').dropna()

            close           = f"{daily.iloc[0]:,.2f}"
            day_pctchg      = daily_chg.round(2)
            week_pctchg     = ((abs(daily.iloc[0]) - abs(weekly.iloc[0])) / weekly.iloc[0] * 100).round(2)
            mtd             = ((abs(daily.iloc[0]) - abs(monthly.iloc[0])) / monthly.iloc[0] * 100).round(2)
            month_pctchg    = ((abs(daily.iloc[0]) - abs(daily.iloc[-1])) / daily.iloc[-1] * 100).round(2)
            ytd             = ((abs(daily.iloc[0]) - abs(yearly.iloc[0])) / yearly.iloc[0] * 100).round(2)

            return close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data for {ticker} - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
    
    print("Max retries reached. Could not fetch data.")
    return "Error", "", "", "", "", ""

def get_other_data(ticker: str, max_retries=3, wait_time=5) -> tuple:
    for retry in range(max_retries):
        try:
            ficc_ticker     = yf.Ticker(ticker)
            daily_data      = ficc_ticker.history(interval="1d", period="21d")['Close']
            weekly_data     = ficc_ticker.history(interval="1wk", period="2wk")['Close']
            monthly_data    = ficc_ticker.history(interval="1mo", period="2mo")['Close']
            yearly_data     = ficc_ticker.history(interval="1mo", period="1y", start=f"{datetime.datetime.now().year-1}-12-01")['Close']

            close           = f"{daily_data.iloc[-1]:,.2f}"
            day_pctchg      = ((daily_data.iloc[-1] - daily_data.iloc[-2]) / daily_data.iloc[-2] * 100).round(2)
            week_pctchg     = ((weekly_data.iloc[-1] - weekly_data.iloc[-2]) / weekly_data.iloc[-2] * 100).round(2)
            mtd             = ((monthly_data.iloc[-1] - monthly_data.iloc[-2]) / monthly_data.iloc[-2] * 100).round(2)
            month_pctchg    = ((daily_data.iloc[-1] - daily_data.iloc[0]) / daily_data.iloc[0] * 100).round(2)
            ytd             = ((yearly_data.iloc[-1] - yearly_data.iloc[0]) / yearly_data.iloc[0] * 100).round(2)

            return close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data for {ticker} - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)

    print("Max retries reached. Could not fetch data.")
    return "Error", "", "", "", "", ""

def get_all_ficc_data() -> list[list]:
    header                  = ["Category", "Close(pt)", "1D(%)", "1W(%)", "MTD(%)", "1M(%)", "YTD(%)"]
    data                    = [header]

    for key, ticker in tqdm(ficc_symbol.items(), desc="Getting FICC Data"):
        if key in ["US02Y", "US10Y", "US10Y-2YS"]:
            close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd = us_yield(ticker)
        else:
            close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd = get_other_data(ticker)
        data.append([key, close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd])

    return data
