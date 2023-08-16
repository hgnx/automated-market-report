import os
import time
import yfinance as yf
import plotly.graph_objects as go
from tqdm import tqdm
from tools.etfs import get_etf_data, etfs_symbol

def create_nasdaq_graph(filename, max_retries=3, wait_time=5):
    for retry in range(max_retries):
        try:
            IXIC            = round(yf.Ticker("^IXIC").history(period="1d", interval="1h")['Close'], 2)
            IXIC.index      = IXIC.index.tz_localize(None)
            fig             = go.Figure(data=go.Scatter(x=IXIC.index, y=IXIC.values, mode='lines'))
            fig.update_layout(title="NASDAQ Intraday Change",
                              xaxis_title="",
                              xaxis=dict(tickformat='%H:%M'),
                              width=600, height=400)
            fig.write_image(filename)
            break
        
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data for ^IXIC - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
    else:
        print("Max retries reached. Could not fetch data.")

def create_sp500_graph(filename, max_retries=3, wait_time=5):
    for retry in range(max_retries):
        try:
            GSPC            = round(yf.Ticker("^GSPC").history(period="1d", interval="1h")['Close'], 2)
            GSPC.index      = GSPC.index.tz_localize(None)
            fig             = go.Figure(data=go.Scatter(x=GSPC.index, y=GSPC.values, mode='lines'))
            fig.update_layout(title="S&P500 Intraday Change",
                              xaxis_title="",
                              xaxis=dict(tickformat='%H:%M'),
                              width=600, height=400)
            fig.write_image(filename)
            break
        
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data for ^GSPC - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
    else:
        print("Max retries reached. Could not fetch data.")

def create_sector_change_graph(filename):
    sectors                 = ['IT', 'Healthcare', 'Financials', 'Consumer Discretionary', 'Communication Services',
                                'Industrials', 'Consumer Staples', 'Energy', 'Utilities', 'Real Estate', 'Materials']
    changes                 = [get_etf_data(etfs_symbol[sector]) for sector in tqdm(sectors, desc="Getting ETFs Data")]

    fig                     = go.Figure([go.Bar(x=sectors, y=changes)])
    fig.update_layout(title="Sector Change",
                      width=600, height=400)
    fig.write_image(filename)

def create_plots():
    current_dir             = os.path.dirname(os.path.abspath(__file__))
    root_dir                = os.path.dirname(current_dir)
    assets_dir              = os.path.join(root_dir, 'assets')

    create_nasdaq_graph(os.path.join(assets_dir, "nasdaq.png"))
    create_sp500_graph(os.path.join(assets_dir, "sp500.png"))
    create_sector_change_graph(os.path.join(assets_dir, "sectors.png"))