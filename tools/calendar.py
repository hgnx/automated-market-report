import pandas as pd
import urllib.request as urllib

def is_valid_value(value):
    str_value               = str(value)
    return not pd.isna(value) and any(c.isdigit() for c in str_value) and len(str_value) <= 10

def fetch_data(url, user_agent):
    opener                  = urllib.build_opener()
    opener.addheaders       = [('User-Agent', user_agent)]
    response                = opener.open(url)
    return response.read()

def process_data(raw_data):
    calendar                = pd.read_html(raw_data)[0].iloc[1:-1]
    calendar                = calendar[['Time', 'Cur.', 'Event', 'Forecast', 'Previous']]
    calendar['Cur.']        = calendar['Cur.'].fillna('-')
    calendar['Forecast']    = calendar['Forecast'].apply(lambda x: x if is_valid_value(x) else '-')
    calendar['Previous']    = calendar['Previous'].apply(lambda x: x if is_valid_value(x) else '-')
    return [["Time (UTC)", "Currency", "Event", "Forecast", "Previous"]] + calendar.values.tolist()

def get_all_economic_data():
    URL                     = "https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=3&features=datepicker,filters&countries=110,43,17,42,5,178,32,12,26,36,4,72,10,14,48,35,37,6,122,41,22,11,25,39&calType=day&timeZone=14&lang=01"
    USER_AGENT              = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    raw_data                = fetch_data(URL, USER_AGENT)
    return process_data(raw_data)
