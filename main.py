import data_download as dd
import data_plotting as dplt
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Запуск программы")
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца) или 'custom' для указания дат: ")

    if period.lower() == 'custom':
        start_date = input("Введите дату начала (в формате YYYY-MM-DD): ")
        end_date = input("Введите дату окончания (в формате YYYY-MM-DD): ")
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)
    else:
        stock_data = dd.fetch_stock_data(ticker, period=period)

    threshold = float(input("Введите порог колебаний в процентах (например, 10 для 10%): "))
    csv_filename = input("Введите имя файла для экспорта данных в CSV (например, 'data.csv'): ")
    style = input("Введите стиль оформления графика (например, 'seaborn', 'ggplot', 'default'): ")

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Calculate RSI
    stock_data = dd.calculate_rsi(stock_data)

    # Calculate MACD
    stock_data = dd.calculate_macd(stock_data)

    # Calculate standard deviation
    stock_data = dd.calculate_standard_deviation(stock_data)

    # Calculate and display average price
    dd.calculate_and_display_average_price(stock_data)

    # Notify if strong fluctuations
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Export data to CSV
    dd.export_data_to_csv(stock_data, csv_filename)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period, style=style)

    # Create interactive plot
    dplt.create_interactive_plot(stock_data, ticker)

    logging.info("Программа завершена")

if __name__ == "__main__":
    main()