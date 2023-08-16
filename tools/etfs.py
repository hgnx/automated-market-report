import yfinance as yf
import time

def get_etf_data(ETF, max_retries=3, wait_time=5):
    for retry in range(max_retries):
        try:
            data            = yf.Ticker(ETF).history(interval="1d", period="2d")['Close'].round(2)
                
            if not data.empty:
                return round((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100, 2)
            
            print(f"No data available for {ETF}.")
            break
                
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data for {ETF} - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
    
    print("Max retries reached. Could not fetch data.")
    return None



etfs_symbol                 = {
                                "IT"                        : "XLK",
                                "Healthcare"                : "XLV",
                                "Financials"                : "XLF",
                                "Consumer Discretionary"    : "XLY",
                                "Communication Services"    : "XLC",
                                "Industrials"               : "XLI",
                                "Consumer Staples"          : "XLP",
                                "Energy"                    : "XLE",
                                "Utilities"                 : "XLU",
                                "Real Estate"               : "XLRE",
                                "Materials"                 : "XLB"
                            }