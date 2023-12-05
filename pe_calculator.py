import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from requests import get
import yfinance as yf
import time
import asyncio
import aiohttp
import yfinance as yf

def get_sp500_stocks_from_wikipedia():

    # URL of the Wikipedia page to scrape
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})

    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            data.append({
                'Symbol': cols[0].text.strip(),
                'Security': cols[1].text.strip(),
                'SEC Filings': cols[2].text.strip(),
                'GICS Sector': cols[3].text.strip(),
                'GICS Sub-Industry': cols[4].text.strip(),
                'Headquarters Location': cols[5].text.strip(),
                'Date First Added': cols[6].text.strip(),
                'CIK': cols[7].text.strip(),
            })

    symbols = [i["Symbol"] for i in data]

    return symbols

def calculate_sp500_pe():

    tickers = [i.replace('.','-') for i in get_sp500_stocks_from_wikipedia()]

    async def fetch_stock_data(session, ticker):
        try:
            stock = yf.Ticker(ticker)
            eps_ttm = stock.info.get('trailingEps', 'Data not available')
            latest_close_price = stock.history(period="1d")['Close'].iloc[-1]
            return ticker, latest_close_price, eps_ttm
        except Exception as e:
            return ticker, 'Error', 'Error'

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_stock_data(session, ticker) for ticker in tickers]
            results = await asyncio.gather(*tasks)
            sum_stock_price = sum(float(r[1]) for r in results if isinstance(r[1], float))
            sum_eps = sum(float(r[2]) for r in results if isinstance(r[2], float))
            for result in results:
                print(f"{result[0]}\t{result[1]}\t{result[2]}")
            print('')
            print(round(sum_stock_price,2))
            print(round(sum_eps,2))
            print(f"PE Ratio: {round(sum_stock_price/sum_eps,2)}")



    asyncio.run(main())



def calculate_nasdaq100_pe():

    tickers = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'META', 'AVGO', 'GOOGL', 'GOOG', 'TSLA', 'ADBE', 'COST', 'PEP', 'NFLX', 'AMD', 'CSCO', 'INTC', 'TMUS', 'CMCSA', 'INTU', 'QCOM', 'AMGN', 'TXN', 'HON', 'AMAT', 'SBUX', 'BKNG', 'ISRG', 'MDLZ', 'ADP', 'LRCX', 'GILD', 'VRTX', 'ADI', 'REGN', 'MU', 'SNPS', 'PANW', 'PDD', 'MELI', 'KLAC', 'CDNS', 'CSX', 'MAR', 'PYPL', 'CHTR', 'ORLY', 'ASML', 'MNST', 'CTAS', 'ABNB', 'LULU', 'NXPI', 'CPRT', 'WDAY', 'MRVL', 'PCAR', 'CRWD', 'KDP', 'MCHP', 'ROST', 'ODFL', 'ADSK', 'DXCM', 'PAYX', 'KHC', 'FTNT', 'AEP', 'SGEN', 'IDXX', 'CEG', 'EXC', 'AZN', 'EA', 'CTSH', 'VRSK', 'FAST', 'CSGP', 'BKR', 'DDOG', 'BIIB', 'GEHC', 'XEL', 'GFS', 'TTD', 'MRNA', 'ON', 'ZS', 'TEAM', 'FANG', 'WBD', 'ANSS', 'DLTR', 'EBAY', 'SIRI', 'WBA', 'ALGN', 'ZM', 'ILMN', 'ENPH', 'JD', 'LCID']

    async def fetch_stock_data(session, ticker):
        try:
            stock = yf.Ticker(ticker)
            eps_ttm = stock.info.get('trailingEps', 'Data not available')
            latest_close_price = stock.history(period="1d")['Close'].iloc[-1]
            return ticker, latest_close_price, eps_ttm
        except Exception as e:
            return ticker, 'Error', 'Error'

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_stock_data(session, ticker) for ticker in tickers]
            results = await asyncio.gather(*tasks)
            sum_stock_price = sum(float(r[1]) for r in results if isinstance(r[1], float))
            sum_eps = sum(float(r[2]) for r in results if isinstance(r[2], float))
            for result in results:
                print(f"{result[0]}\t{result[1]}\t{result[2]}")
            print('')
            print(round(sum_stock_price,2))
            print(round(sum_eps,2))
            print(f"PE Ratio: {round(sum_stock_price/sum_eps,2)}")

    asyncio.run(main())


calculate_sp500_pe()