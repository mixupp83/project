import yfinance as yf
import pandas as pd
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker, period='1mo'):
    """
    Загружает исторические данные акций с Yahoo Finance.

    :param ticker: Символ акции (например, 'AAPL' для Apple Inc).
    :param period: Период данных (например, '1mo' для одного месяца).
    :return: DataFrame с историческими данными.
    """
    logging.info(f"Загрузка данных для тикера {ticker} за период {period}")
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    logging.info(f"Данные для тикера {ticker} успешно загружены")
    return data

def add_moving_average(data, window_size=5):
    """
    Добавляет скользящее среднее к данным.

    :param data: DataFrame с историческими данными.
    :param window_size: Размер окна для скользящего среднего.
    :return: DataFrame с добавленным скользящим средним.
    """
    logging.info(f"Добавление скользящего среднего с размером окна {window_size}")
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    logging.info("Скользящее среднее успешно добавлено")
    return data

def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия за период.

    :param data: DataFrame с историческими данными.
    """
    if 'Close' in data.columns:
        average_price = data['Close'].mean()
        logging.info(f"Средняя цена закрытия за период: {average_price:.2f}")
        print(f"Средняя цена закрытия за период: {average_price:.2f}")
    else:
        logging.warning("Столбец 'Close' отсутствует в данных.")
        print("Столбец 'Close' отсутствует в данных.")

def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

    :param data: DataFrame с историческими данными.
    :param threshold: Порог колебаний в процентах.
    """
    if 'Close' in data.columns:
        max_price = data['Close'].max()
        min_price = data['Close'].min()
        fluctuation = (max_price - min_price) / min_price * 100
        if fluctuation > threshold:
            logging.warning(f"Внимание! Сильные колебания цены: {fluctuation:.2f}% (порог: {threshold}%)")
            print(f"Внимание! Сильные колебания цены: {fluctuation:.2f}% (порог: {threshold}%)")
        else:
            logging.info(f"Колебания цены в пределах нормы: {fluctuation:.2f}% (порог: {threshold}%)")
            print(f"Колебания цены в пределах нормы: {fluctuation:.2f}% (порог: {threshold}%)")
    else:
        logging.warning("Столбец 'Close' отсутствует в данных.")
        print("Столбец 'Close' отсутствует в данных.")
