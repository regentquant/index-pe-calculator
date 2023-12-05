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


calculate_nasdaq100_pe()
