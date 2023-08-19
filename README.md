# Automated Stock Market Report Generator
The Automated Stock Market Report Generator is a Python script designed to streamline the fetching of data from multiple sources and produce a detailed daily report in PDF format. This report primarily focuses on the stock market's performance and associated data.

In the dynamic world of financial markets, staying informed is crucial. This script consolidates data pertaining to global market indices, currency and commodity, leading gainers and losers, forthcoming economic events, and pivotal financial news headlines.

## Features
- **Data Aggregation**: The script fetches data from diverse sources including Yahoo Finance, FRED, CNN, Investing.com, Reuters, and Financial Times.
- **PDF Generation**: The fetched data is compiled into a structured PDF report for easy consumption.
- **Customizable Headers**: The report features customizable headers including company information, author details, and the current date.
- **Informative Tables**: Tables present data on global market indices, FICC data, top gainers, top losers, economic calendar events, and news headlines.
- **Styling**: The report is formatted with distinct styles for sections, headers, captions, and content.
- **URL Shortener Integration**: News URLs are automatically shortened for concise design.

## Data Sources
The script fetches data from the following sources:
| Data Categories        | Description                                | Provider              | Library/Tool       |
|------------------------|--------------------------------------------|-----------------------|--------------------|
| Global Market Indices  | Global stock market indices data           | Yahoo Finance         | `yfinance`         |
| FICC (w/o US Yields)   | Currencies, and Commodities data           | Yahoo Finance         | `yfinance`         |
| US Treasury Yields     | US Treasury yield data (*Need API*)        | FRED                  | `fredapi`          |
| ETFs                   | ETF data categorized by GICS groups        | Yahoo Finance         | `yfinance`         |
| Top Gainers/Losers     | Top gaining and losing stocks data         | CNN                   | N/A                |
| Economic Calendar      | Daily upcoming economic events data        | Investing.com         | N/A                |
| News                   | Financial news headlines                   | Reuters, Financial Times | N/A             |
* For the Economic Calendar, only events with an importance level of 3 are fetched. However, it has been observed that if there are no events with an importance level of 3 from Investing.com's URL, such as on weekends, events for the entire week are retrieved. If this issue occurs on weekdays as well, I will look into a solution.

## Setup
- Before running the main script (`main.py`), configure your FRED API key using the `setup.py` script. You will be prompted to provide your FRED API key, which will be stored in a `config.ini` file for the main script to reference.
- If you do not possess a FRED API key, please register for an account on FRED's website. Upon registration, you will be able to obtain the API key at no cost: https://fred.stlouisfed.org.

## Installation and Usage
1. Download the project code.
```
git clone https://github.com/hgnx/automated-market-report.git
```

2. Install the required libraries.
```
pip install -r requirements.txt
```

3. Run the setup script to configure your FRED API key.
```
python setup.py
```

4. Within `main.py`, allocate the company's name and the author's details to their respective variables.
   - `COMPANY_NAME`: Represents the name of the company. Utilize the `<br />` tag to facilitate line breaks. It's advisable to limit this to a maximum of 2 lines.
   - `AUTHOR`: The name of the author.
   - `AUTHOR_EMAIL`: The email address of the author.

5. Run the main script.
```
python main.py
```

6. Check the generated PDF in the same folder as `main.py`.

## Future Improvements
This is the initial release. I am considering several enhancements and features for the upcoming versions:
- Global Market Indices & FICC:
  - [ ] Implement a data fetching mechanism that respects the user's timezone.
- News:
  - [ ] Introduce an additional news source.
  - [ ] Incorporate sentiment analysis.
- Economic Calendar:
  - [ ] Address the issue of fetching all events when there are no events with an importance level of 3 (e.g., on weekends).

As more ideas for improvement arise, they will be added to this list.

Kindly note that my availability to this project is limited; hence, updates may be sporadic.

## Disclaimer
The script or information provided in this document/repository is for informational purposes only and should not be used as the basis for any financial decisions. I take no responsibility for any personal financial loss. Use this script at your own risk.

I make no warranties or representations regarding the accuracy, relevance, or completeness of any data, irrespective of specific indications or implications present within any code in this repository. I am not liable for any inaccuracies, errors, or omissions in the content provided.