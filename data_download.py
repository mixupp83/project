import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    if 'Close' in data.columns:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия за период: {average_price:.2f}")
    else:
        print("Столбец 'Close' отсутствует в данных.")

def notify_if_strong_fluctuations(data, threshold):
    if 'Close' in data.columns:
        max_price = data['Close'].max()
        min_price = data['Close'].min()
        fluctuation = (max_price - min_price) / min_price * 100
        if fluctuation > threshold:
            print(f"Внимание! Сильные колебания цены: {fluctuation:.2f}% (порог: {threshold}%)")
        else:
            print(f"Колебания цены в пределах нормы: {fluctuation:.2f}% (порог: {threshold}%)")
    else:
        print("Столбец 'Close' отсутствует в данных.")
