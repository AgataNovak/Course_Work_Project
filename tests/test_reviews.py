import json
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import (cards_info, external_api_currency,
                       external_api_stock_prices, get_currencies_rates_json,
                       get_stocks_rates_json, get_transactions_data,
                       get_user_currencies, get_user_stocks,
                       greetings_by_daytime, period, top_transactions)


class TestGreetingsByDaytime(unittest.TestCase):

    def test_greetings_by_daytime(self):
        assert greetings_by_daytime("2024.06.21 09:30:30") == {
            "greetings": "Доброе утро!"
        }
        assert greetings_by_daytime("2024.06.21 13:00:50") == {
            "greetings": "Добрый день!"
        }
        assert greetings_by_daytime("2003.01.09 19:55:00") == {
            "greetings": "Добрый вечер!"
        }
        assert greetings_by_daytime("2003.01.09 01:55:00") == {
            "greetings": "Доброй ночи!"
        }


class GetTransactionsData(unittest.TestCase):

    data = {
        "Дата платежа": ["2021.12.31 16:30:24"],
        "Номер карты": ["*7358"],
        "Статус операции": ["OK"],
        "Сумма операции": [-16000],
        "Категория": ["Супермаркеты"],
    }

    df = pd.DataFrame(data)

    df.to_excel("test.xlsx", index=False)

    @patch("pandas.read_excel", return_value=df)
    def test_get_transactions_data(self, mock_read_excel: MagicMock) -> None:
        result = get_transactions_data()
        self.assertEqual(
            result,
            {
                "Дата платежа": {0: "2021.12.31 16:30:24"},
                "Номер карты": {0: "*7358"},
                "Статус операции": {0: "OK"},
                "Сумма операции": {0: -16000},
                "Категория": {0: "Супермаркеты"},
            },
        )

    @patch("pandas.read_excel")
    def test_get_transactions_data_empty(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame({})
        transactions = get_transactions_data()
        self.assertEqual(transactions, {})


class TestCardsInfo(unittest.TestCase):

    def test_cards_info(self):
        data = {
            "Дата платежа": {0: "2021.12.31 16:30:24"},
            "Номер карты": {0: "*7358"},
            "Статус операции": {0: "OK"},
            "Сумма операции": {0: -16000},
            "Категория": {0: "Супермаркеты"},
        }
        result = {
            "cards": [
                {"last_digits": "7358", "total_spent": "16000", "cashback": "160.0"}
            ]
        }
        assert cards_info(data_excel=data) == result


class TestPeriod(unittest.TestCase):

    def test_period(self):
        date = "2023.12.30 23:23:23"
        result = [
            "01.12.2023",
            "02.12.2023",
            "03.12.2023",
            "04.12.2023",
            "05.12.2023",
            "06.12.2023",
            "07.12.2023",
            "08.12.2023",
            "09.12.2023",
            "10.12.2023",
            "11.12.2023",
            "12.12.2023",
            "13.12.2023",
            "14.12.2023",
            "15.12.2023",
            "16.12.2023",
            "17.12.2023",
            "18.12.2023",
            "19.12.2023",
            "20.12.2023",
            "21.12.2023",
            "22.12.2023",
            "23.12.2023",
            "24.12.2023",
            "25.12.2023",
            "26.12.2023",
            "27.12.2023",
            "28.12.2023",
            "29.12.2023",
            "30.12.2023",
        ]
        assert period(date) == result


class TestTopTransactions(unittest.TestCase):

    def test_top_transactions(self):
        data = {
            "Дата платежа": {0: "2021.12.29 16:30:24"},
            "Номер карты": {0: "*7358"},
            "Статус": {0: "OK"},
            "Сумма операции с округлением": {0: -16000},
            "Сумма операции": {0: -16000},
            "Категория": {0: "Супермаркеты"},
            "Описание": {0: "Колхоз"},
        }
        date = "2021.12.31 16:30:24"
        result = {"top transactions": []}
        assert top_transactions(date, data) == result


class TestExternalApiCurrency(unittest.TestCase):

    @patch("requests.get")
    def test_external_api_currency(self, mock_get):
        mock_get.return_value.status_code = "200"
        mock_get.return_value.json.return_value = {
            "USD": 1,
            "EUR": 1.076,
            "RUB": 83.356,
        }
        assert external_api_currency("test_api_key") == {
            "USD": 1,
            "EUR": 1.076,
            "RUB": 83.356,
        }

    @patch("requests.get")
    def test_external_api_refused_response(self, mock_get):
        mock_get.return_value.status_code = "401"
        assert external_api_currency("test_api_key") == []


class TestExternalApiStockPrices(unittest.TestCase):

    @patch("requests.get")
    def test_external_api_stock_prices(self, mock_get):
        stock_list = ["APPL"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {0: {"sign": "APPL", "mark": 260.00}}
        }
        assert external_api_stock_prices(stock_list, "test_api_key") == [
            {"price": 260.0, "stock": "APPL"}
        ]

    @patch("requests.get")
    def test_external_api_stock_prices_refused_response(self, mock_get):
        stock_list = ["APPL", "BIM"]
        mock_get.return_value.status_code = "401"
        assert external_api_stock_prices(stock_list, "test_api_key") == []


class TestGetUserCurrencies(unittest.TestCase):

    @patch("builtins.open")
    def test_get_user_currencies(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
            [
                {
                    "user_currencies": ["USD", "EUR", "GBP"],
                    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
                }
            ]
        )
        result = ["USD", "EUR", "GBP"]
        assert get_user_currencies("test_path_to_json") == result

    def test_get_user_currencies_does_not_exist(self):
        assert get_user_currencies("test_path_to_json_does_not_exist") == []


class TestGetUserStocks(unittest.TestCase):

    @patch("builtins.open")
    def test_get_user_stocks(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
            [
                {
                    "user_currencies": ["USD", "EUR", "GBP"],
                    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
                }
            ]
        )
        result = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        assert get_user_stocks("test_path_to_json") == result

    def test_get_user_stocks_does_not_exist(self):
        assert get_user_stocks("test_path_to_json_does_not_exist") == []


class TestGetStockRatesJson(unittest.TestCase):

    def test_get_stocks_rates(self):
        stock_dict = [{"stock": "APPL", "price": 260.0}]
        assert get_stocks_rates_json(stock_dict) == {
            "stock_prices": [{"stock": "APPL", "price": 260.0}]
        }


class TestGetCurrenciesRatesJson(unittest.TestCase):

    def test_get_currencies_rates_json(self):
        currency_list = ["USD", "EUR"]
        currency_response_json = {"data": {"USD": 1, "EUR": 1.076, "RUB": 83.356}}
        result = {
            "currency_rates": [
                {"currency": "USD", "rate": 83.36},
                {"currency": "EUR", "rate": 77.47},
            ]
        }
        assert (
            get_currencies_rates_json(currency_list, currency_response_json) == result
        )
