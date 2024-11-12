import matplotlib.pyplot as plt
import pandas as pd
import logging
import plotly.graph_objs as go

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Создает и сохраняет график цены акций, скользящего среднего, RSI, MACD и стандартного отклонения.

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

    plt.figure(figsize=(15, 12))

    # График цены и скользящего среднего
    plt.subplot(4, 1, 1)
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
    plt.subplot(4, 1, 2)
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
    plt.subplot(4, 1, 3)
    if 'MACD' in data.columns and 'Signal' in data.columns:
        plt.plot(data.index, data['MACD'], label='MACD')
        plt.plot(data.index, data['Signal'], label='Signal')
        plt.title('Moving Average Convergence Divergence (MACD)')
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()
    else:
        logging.warning("Столбцы 'MACD' или 'Signal' отсутствуют в данных.")

    # График стандартного отклонения
    plt.subplot(4, 1, 4)
    if 'Std_Dev' in data.columns:
        plt.plot(data.index, data['Std_Dev'], label='Standard Deviation')
        plt.title('Standard Deviation of Close Price')
        plt.xlabel("Дата")
        plt.ylabel("Standard Deviation")
        plt.legend()
    else:
        logging.warning("Столбец 'Std_Dev' отсутствует в данных.")

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    logging.info(f"График сохранен как {filename}")
    print(f"График сохранен как {filename}")

def create_interactive_plot(data, ticker):
    """
    Создает интерактивный график цены акций с использованием plotly.

    :param data: DataFrame с историческими данными.
    :param ticker: Символ акции.
    """
    logging.info(f"Создание интерактивного графика для тикера {ticker}")

    # Вычисление среднего значения колонки 'Close'
    average_close = data['Close'].mean()
    logging.info(f"Среднее значение 'Close' для тикера {ticker}: {average_close:.2f}")
    print(f"Среднее значение 'Close' для тикера {ticker}: {average_close:.2f}")

    # Создание графика
    fig = go.Figure()

    # Добавление линии цены закрытия
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))

    # Добавление линии среднего значения
    fig.add_trace(go.Scatter(x=data.index, y=[average_close]*len(data), mode='lines', name='Average Close', line=dict(dash='dash')))

    # Настройка макета графика
    fig.update_layout(
        title=f"{ticker} Интерактивный график цены акций",
        xaxis_title="Дата",
        yaxis_title="Цена",
        legend_title="Легенда",
        hovermode="x unified"
    )

    # Отображение графика
    fig.show()

    logging.info(f"Интерактивный график для тикера {ticker} успешно создан")