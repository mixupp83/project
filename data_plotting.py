import matplotlib.pyplot as plt
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Создает и сохраняет график цены акций, скользящего среднего, RSI и MACD.

    :param data: DataFrame с историческими данными.
    :param ticker: Символ акции.
    :param period: Период данных.
    :param filename: Имя файла для сохранения графика.
    :param style: Стиль оформления графика (например, 'seaborn', 'ggplot', 'default').
    """
    logging.info(f"Создание графика для тикера {ticker} за период {period} со стилем {style}")

    # Проверяем, является ли стиль допустимым
    if style not in plt.style.available:
        logging.warning(f"Стиль '{style}' не найден. Используется стиль по умолчанию.")
        style = 'default'

    # Применяем выбранный стиль
    plt.style.use(style)

    plt.figure(figsize=(15, 10))

    # График цены и скользящего среднего
    plt.subplot(3, 1, 1)
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            logging.error("Информация о дате отсутствует или не имеет распознаваемого формата.")
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График RSI
    plt.subplot(3, 1, 2)
    if 'RSI' in data.columns:
        plt.plot(data.index, data['RSI'], label='RSI')
        plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
        plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
        plt.title('Relative Strength Index (RSI)')
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()
    else:
        logging.warning("Столбец 'RSI' отсутствует в данных.")

    # График MACD
    plt.subplot(3, 1, 3)
    if 'MACD' in data.columns and 'Signal' in data.columns:
        plt.plot(data.index, data['MACD'], label='MACD')
        plt.plot(data.index, data['Signal'], label='Signal')
        plt.title('Moving Average Convergence Divergence (MACD)')
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()
    else:
        logging.warning("Столбцы 'MACD' или 'Signal' отсутствуют в данных.")

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    logging.info(f"График сохранен как {filename}")
    print(f"График сохранен как {filename}")
