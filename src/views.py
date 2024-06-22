import os

from dotenv import load_dotenv

from src.logger import setup_logger
from src.utils import (cards_info, external_api_currency,
                       external_api_stock_prices, get_currencies_rates_json,
                       get_stocks_rates_json, get_transactions_data,
                       get_user_currencies, get_user_stocks,
                       greetings_by_daytime, top_transactions)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_logs = os.path.join(current_dir, "../logs", "views.log")
logger = setup_logger("views", file_path_logs)


load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCK_PRICES")
data_excel = get_transactions_data()
current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_user_json = os.path.join(current_dir, "../data", "user_settings.json")


def main_page_json_response(date):
    """Функция принимает дату и возвращает  JSON ответ с приветствием, информацией по картам, топ-5 транзакций,
    курс валют и стоимость акций"""

    logger.info("Запущена функция main_page_json_response")

    stock_list = get_user_stocks(path_to_user_json)
    currencies_list = get_user_currencies(path_to_user_json)
    currency_response_json = external_api_currency(api_key_currency)
    stock_response_json = external_api_stock_prices(stock_list, api_key_stocks)
    greetings = greetings_by_daytime(date)
    cards = cards_info(data_excel)
    top_trans = top_transactions(date, data_excel)
    currency_rates = get_currencies_rates_json(currencies_list, currency_response_json)
    stock_rates = get_stocks_rates_json(stock_response_json)

    response_json = {}
    response_json.update(greetings)
    response_json.update(cards)
    response_json.update(top_trans)
    response_json.update(currency_rates)
    response_json.update(stock_rates)

    logger.info("Функция main_page_json_response вернула JSON ответ")
    return response_json


if __name__ == "__main__":
    print(main_page_json_response("2021.12.31 20:13:30"))
