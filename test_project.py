import unittest
import pandas as pd
import data_download as dd
import data_plotting as dplt
import os

class TestStockDataAnalysis(unittest.TestCase):

    def setUp(self):
        self.ticker = 'AAPL'
        self.period = '1mo'
        self.threshold = 10
        self.csv_filename = 'test_data.csv'

    def test_fetch_stock_data(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn('Close', data.columns)

    def test_add_moving_average(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        data = dd.add_moving_average(data)
        self.assertIn('Moving_Average', data.columns)

    def test_calculate_rsi(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        data = dd.calculate_rsi(data)
        self.assertIn('RSI', data.columns)

    def test_calculate_macd(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        data = dd.calculate_macd(data)
        self.assertIn('MACD', data.columns)
        self.assertIn('Signal', data.columns)

    def test_calculate_and_display_average_price(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        dd.calculate_and_display_average_price(data)
        # Проверка, что функция не вызывает ошибок
        self.assertTrue(True)

    def test_notify_if_strong_fluctuations(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        dd.notify_if_strong_fluctuations(data, self.threshold)
        # Проверка, что функция не вызывает ошибок
        self.assertTrue(True)

    def test_export_data_to_csv(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        dd.export_data_to_csv(data, self.csv_filename)
        # Сравниваем данные, игнорируя индексы и типы данных
        data_from_csv = pd.read_csv(self.csv_filename).reset_index(drop=True)
        data_to_compare = data.reset_index(drop=True)
        # Выбираем только числовые столбцы для сравнения
        data_from_csv_numeric = data_from_csv.select_dtypes(include=['number'])
        data_to_compare_numeric = data_to_compare.select_dtypes(include=['number'])
        self.assertTrue(data_from_csv_numeric.equals(data_to_compare_numeric))
        # Удаляем временный CSV файл после теста
        os.remove(self.csv_filename)

    def test_create_and_save_plot(self):
        data = dd.fetch_stock_data(self.ticker, self.period)
        data = dd.add_moving_average(data)
        data = dd.calculate_rsi(data)
        data = dd.calculate_macd(data)
        dplt.create_and_save_plot(data, self.ticker, self.period)
        # Проверка, что функция не вызывает ошибок
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()