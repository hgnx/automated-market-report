import pandas as pd

URL                         = "https://money.cnn.com/data/hotstocks/"

def get_similar_column_name(df, col_str):
    if similar_cols         := [col for col in df.columns if col_str in col.replace("\xa0", " ")]:
        return similar_cols[0]
    else:
        raise ValueError(f"Cannot find a column similar to {col_str}")

def process_data(df):
    pct_chg_col             = get_similar_column_name(df, "% Change")
    return [
        [
            row['Company'].split(' ', 1)[0],
            row['Company'].split(' ', 1)[1],
            row['Price'],
            str(row['Change']).lstrip('+'),
            str(row[pct_chg_col]).rstrip('%').lstrip('+')
        ] for _, row in df.to_dict('index').items()
    ]

def get_top_movers_data():
    tables                  = pd.read_html(URL, encoding="utf-8")
    gainers_data            = [["Ticker", "Company", "Price", "Change", "Change(%)"]] + process_data(tables[1])
    losers_data             = [["Ticker", "Company", "Price", "Change", "Change(%)"]] + process_data(tables[2])
    
    return gainers_data, losers_data