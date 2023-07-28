import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

def create_nasdaq_graph(filename):
    time_range                  = pd.date_range(start='9:00', end='16:00', freq='1H')
    values                      = np.array([13000, 12980, 13020, 13050, 13070, 13040, 13080, 13090])
    
    fig                         = go.Figure(data=go.Scatter(x=time_range, y=values, mode='lines'))
    fig.update_layout(title="NASDAQ Intraday Change",
                      xaxis_title="",
                      xaxis=dict(tickformat='%H:%M'),
                      width=600, height=400)
    fig.write_image(filename)

def create_sp500_graph(filename):
    time_range                  = pd.date_range(start='9:00', end='16:00', freq='1H')
    values                      = np.array([4500, 4480, 4490, 4470, 4520, 4540, 4490, 4510])
    
    fig                         = go.Figure(data=go.Scatter(x=time_range, y=values, mode='lines'))
    fig.update_layout(title="S&P500 Intraday Change",
                      xaxis_title="",
                      xaxis=dict(tickformat='%H:%M'),
                      width=600, height=400)
    fig.write_image(filename)

def create_sector_change_graph(filename):
    sectors                     = ['IT', 'Healthcare', 'Financials', 'Consumer Discretionary', 'Communication Services',
                                    'Industrials', 'Consumer Staples', 'Energy', 'Utilities', 'Real Estate', 'Materials']
    changes                     = np.array([-1.2, 0.5, 1.8, 0.3, -0.7, -1.5, 0.9, -2.0, 1.2, 0.1, -0.8])

    fig                         = go.Figure([go.Bar(x=sectors, y=changes)])
    fig.update_layout(title="Sector Change",
                      width=600, height=400)
    fig.write_image(filename)

def create_plots():
    current_dir                 = os.path.dirname(os.path.abspath(__file__))
    root_dir                    = os.path.dirname(current_dir)
    assets_dir                  = os.path.join(root_dir, 'assets')

    create_nasdaq_graph(os.path.join(assets_dir, "nasdaq.png"))
    create_sp500_graph(os.path.join(assets_dir, "sp500.png"))
    create_sector_change_graph(os.path.join(assets_dir, "sectors.png"))