import yfinance as yf
import datetime
import time
from tqdm import tqdm

indices_symbol              = {
                                "DOW"           : "^DJI",
                                "S&P500"        : "^GSPC",
                                "NASDAQ"        : "^IXIC",
                                "RUSSELL2000"   : "^RUT",
                                "STOXX600 (EU)" : "^STOXX",
                                "FTSE100 (UK)"  : "^FTSE",
                                "CAC40 (FR)"    : "^FCHI",
                                "DAX (DE)"      : "^GDAXI",
                                "SSE (CN)"      : "000001.SS",
                                "HANGSENG (HK)" : "^HSI",
                                "TSEC (TW)"     : "^TWII",
                                "NIKKEI225 (JP)": "^N225",
                                "KOSPI (KR)"    : "^KS11"
                            }

def get_indices_data(ticker: str, max_retries=3, wait_time=5) -> tuple:
    for retry in range(max_retries):
        try:
            indices_ticker  = yf.Ticker(ticker)
            daily_data      = indices_ticker.history(interval="1d", period="21d")['Close']
            weekly_data     = indices_ticker.history(interval="1wk", period="2wk")['Close']
            monthly_data    = indices_ticker.history(interval="1mo", period="2mo")['Close']
            yearly_data     = indices_ticker.history(interval="1mo", period="1y", start=f"{datetime.datetime.now().year-1}-12-01")['Close']

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

def get_all_indices_data() -> list[list]:
    header                  = ["Indices", "Close(pt)", "1D(%)", "1W(%)", "MTD(%)", "1M(%)", "YTD(%)"]
    data                    = [header]

    for key, ticker in tqdm(indices_symbol.items(), desc="Getting Indices Data"):
        close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd = get_indices_data(ticker)
        data.append([key, close, day_pctchg, week_pctchg, mtd, month_pctchg, ytd])

    return data