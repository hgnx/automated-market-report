import yfinance as yf

def get_etf_data(ETF):
    data                    = yf.Ticker(ETF).history(interval="1d", period="2d")['Close'].round(2)
    return round((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100, 2)

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