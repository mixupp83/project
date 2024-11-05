import yfinance as yf
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    """
    Загружает исторические данные акций с Yahoo Finance.

    :param ticker: Символ акции (например, 'AAPL' для Apple Inc).
    :param period: Период данных (например, '1mo' для одного месяца).
    :param start_date: Дата начала (в формате YYYY-MM-DD).
    :param end_date: Дата окончания (в формате YYYY-MM-DD).
    :return: DataFrame с историческими данными.
    """
    logging.info(f"Загрузка данных для тикера {ticker}")
    stock = yf.Ticker(ticker)
    if period:
        data = stock.history(period=period)
    elif start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
        raise ValueError("Необходимо указать либо период, либо даты начала и окончания.")
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


def calculate_rsi(data, window=14):
    """
    Рассчитывает индекс относительной силы (RSI).

    :param data: DataFrame с историческими данными.
    :param window: Размер окна для расчета RSI.
    :return: DataFrame с добавленным RSI.
    """
    logging.info(f"Расчет RSI с размером окна {window}")
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    logging.info("RSI успешно рассчитан")
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Рассчитывает индикатор MACD.

    :param data: DataFrame с историческими данными.
    :param short_window: Короткий период для расчета EMA.
    :param long_window: Длинный период для расчета EMA.
    :param signal_window: Период для расчета сигнальной линии.
    :return: DataFrame с добавленным MACD.
    """
    logging.info(
        f"Расчет MACD с коротким окном {short_window}, длинным окном {long_window} и сигнальным окном {signal_window}")
    data['EMA_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    logging.info("MACD успешно рассчитан")
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


def export_data_to_csv(data, filename):
    """
    Экспортирует данные в CSV файл.

    :param data: DataFrame с историческими данными.
    :param filename: Имя файла для сохранения.
    """
    logging.info(f"Экспорт данных в файл {filename}")
    data.to_csv(filename)
    logging.info(f"Данные успешно экспортированы в файл {filename}")
