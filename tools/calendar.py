import pandas as pd
import urllib.request as urllib
import time

URL                             = "https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=3&features=datepicker,filters&countries=110,43,17,42,5,178,32,12,26,36,4,72,10,14,48,35,37,6,122,41,22,11,25,39&calType=day&timeZone=14&lang=01"
'''
Timezone: 14(UTC), 88(UTC+9)
Lang: 01(ENG), 18(KOR)
'''
USER_AGENT                      = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

MAX_STRING_LENGTH               = 10
DEFAULT_HEADERS                 = [["Time (UTC)", "Currency", "Event", "Forecast", "Previous"]]

def is_valid_value(value):
    str_value                   = str(value)
    return not pd.isna(value) and any(c.isdigit() for c in str_value) and len(str_value) <= MAX_STRING_LENGTH

def fetch_data(url, user_agent, max_retries=3, wait_time=5):
    for retry in range(max_retries):
        try:
            opener              = urllib.build_opener()
            opener.addheaders   = [('User-Agent', user_agent)]
            response            = opener.open(url)
            return response.read()
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data for calendar- {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)

    print("Max retries reached. Could not fetch data.")
    return None


def extract_and_process_data(raw_data):
    if raw_data is None:
        raise ValueError("Received None as raw data")

    calendar                    = pd.read_html(raw_data)[0].iloc[1:].dropna(subset=['Event'])
    calendar                    = calendar[['Time', 'Cur.', 'Event', 'Forecast', 'Previous']]
    calendar['Cur.']            = calendar['Cur.'].fillna('-')
    calendar['Forecast']        = calendar['Forecast'].apply(lambda x: x if is_valid_value(x) else '-')
    calendar['Previous']        = calendar['Previous'].apply(lambda x: x if is_valid_value(x) else '-')

    return DEFAULT_HEADERS + calendar.values.tolist()

def get_all_economic_data():
    try:
        raw_data                = fetch_data(URL, USER_AGENT)
        processed_data          = extract_and_process_data(raw_data)
        if len(processed_data) > 1:
            return processed_data
        else:
            return DEFAULT_HEADERS + [["", "", "No important event today", "", ""]]
    except Exception as e:
        print(f"Error in get_all_economic_data - {e}")
        return DEFAULT_HEADERS + [["", "", "Error fetching economic calendar", "", ""]]