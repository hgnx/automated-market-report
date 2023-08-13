import os
import yfinance as yf
import plotly.graph_objects as go
from tools.etfs import get_etf_data, etfs_symbol

def create_nasdaq_graph(filename):
    IXIC                    = round(yf.Ticker("^IXIC").history(period="1d", interval="1h")['Close'], 2)
    IXIC.index              = IXIC.index.tz_localize(None)
    fig                     = go.Figure(data=go.Scatter(x=IXIC.index, y=IXIC.values, mode='lines'))
    fig.update_layout(title="NASDAQ Intraday Change",
                      xaxis_title="",
                      xaxis=dict(tickformat='%H:%M'),
                      width=600, height=400)
    fig.write_image(filename)

def create_sp500_graph(filename):
    SPX                     = round(yf.Ticker("^SPX").history(period="1d", interval="1h")['Close'], 2)
    SPX.index = SPX.index.tz_localize(None)
    fig                     = go.Figure(data=go.Scatter(x=SPX.index, y=SPX.values, mode='lines'))
    fig.update_layout(title="S&P500 Intraday Change",
                      xaxis_title="",
                      xaxis=dict(tickformat='%H:%M'),
                      width=600, height=400)
    fig.write_image(filename)

def create_sector_change_graph(filename):
    sectors                 = ['IT', 'Healthcare', 'Financials', 'Consumer Discretionary', 'Communication Services',
                                'Industrials', 'Consumer Staples', 'Energy', 'Utilities', 'Real Estate', 'Materials']
    changes                 = [get_etf_data(etfs_symbol[sector]) for sector in sectors]

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