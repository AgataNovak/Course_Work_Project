import datetime
import json
import os
import re

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

from src.logger import setup_logger

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_logs = os.path.join(current_dir, "../logs", "utils.log")
logger = setup_logger("utils", file_path_logs)


def greetings_by_daytime(date):
    """Функция возвращает приветствие в зависимости от времени суток на данный момент"""

    logger.info("Запущена функция greetings_by_daytime")

    datetime_obj = date
    if int(datetime_obj[-8:-6]) in list(range(5, 12)):
        greeting = "Доброе утро!"
    elif int(datetime_obj[-8:-6]) in list(range(12, 16)):
        greeting = "Добрый день!"
    elif int(datetime_obj[-8:-6]) in list(range(16, 24)):
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"
    greeting = {"greetings": greeting}

    logger.info("Функция greetings_by_daytime успешно вернула JSON ответ")

    return greeting


def get_transactions_data(data):
    """Функция возвращает данные из существующего excel файла"""

    logger.info("Запущена функция get_transactions_data")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_excel = os.path.join(current_dir, "../data", f"{data}")
    with open(path_to_excel, "rb") as excel_file:
        data = pd.read_excel(excel_file)
        data = data.to_dict()

        logger.info("Функция get_transactions_data успешно вернула JSON ответ")
        return data


def cards_info(data_excel):
    """Функция возвращает словарь с данными о картах"""

    logger.info("Запущена функция cards_info")

    data = pd.DataFrame(data_excel)
    not_null_cards = data.loc[data["Номер карты"].notnull()]
    not_null_cards_pay = not_null_cards.loc[not_null_cards["Сумма операции"] < 0]
    operations_grouped = not_null_cards_pay.groupby("Номер карты")
    sum_of_payments = operations_grouped["Сумма операции"].sum()
    cards_dict = sum_of_payments.to_dict()
    new_dict_list = []
    for key, value in cards_dict.items():
        new_dict_list.append(
            {
                "last_digits": key[1:],
                "total_spent": str(value)[1:],
                "cashback": str(round(value / 100, 2))[1:],
            }
        )

    logger.info("Функция cards_info успешно вернула JSON ответ")

    return {"cards": new_dict_list}


def period(date):
    """Функция возвращает перод с начала месяца по указанную дату в виде списка дат"""

    logger.info("Запущена функция period")

    date_obj = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S")
    possible_dates = []
    for i in range(date_obj.day):
        possible_date = date_obj.replace(day=i + 1)
        possible_dates.append(possible_date.strftime("%d.%m.%Y"))

        logger.info("Функция period успешно вернула JSON ответ")

    return possible_dates


def top_transactions(date, data):
    """Функция возвращает словарь с данными о самых крупных траназкциях за указанный месяц"""

    logger.info("Запущена функция top_transactions")

    top_transactions_list = []
    data = pd.DataFrame(data)
    possible_dates = period(date)
    data = data.loc[data["Статус"] == "OK"]
    data = data.sort_values(by="Сумма операции с округлением", ascending=False)
    transactions_in_current_month = data.loc[data["Дата платежа"].isin(possible_dates)]
    data = transactions_in_current_month.head(5)
    dates = []
    amounts = []
    categories = []
    descriptions = []
    data_dates = data["Дата платежа"]
    for item in data_dates:
        dates.append(item)
    data_amounts = data["Сумма операции"]
    for item in data_amounts:
        amounts.append(item)
    data_categories = data["Категория"]
    for item in data_categories:
        categories.append(item)
    data_descriptions = data["Описание"]
    for item in data_descriptions:
        descriptions.append(item)
    for i in range(len(dates)):
        top_transactions_list.append(
            {
                "date": dates[i],
                "amount": amounts[i],
                "category": categories[i],
                "description": descriptions[i],
            }
        )
    top_transactions_dict = {"top transactions": top_transactions_list}

    logger.info("Функция top_transactions успешно вернула JSON ответ")

    return top_transactions_dict


def external_api_currency(api_key):
    """Функция принимает api ключ для валютного api и возвращает словарь с данными о валютах"""

    logger.info("Запущена функция external_api_currency")

    url = "https://api.freecurrencyapi.com/v1/latest"
    headers = CaseInsensitiveDict()
    headers["apikey"] = api_key
    resp = requests.get(url, headers=headers)
    if resp.status_code == "200":

        logger.info("Ответ от стороннего апи валют получен. Код ответа - 200. Успешно.")
        logger.info("Функция external_api_currency успешно вернула JSON ответ")
        return resp.json()
    else:

        logger.error("Ответ от стороннего апи валют неуспешный. Ошибка получения JSON ответа")

        return []


def external_api_stock_prices(stock_list, api_key):
    """Функция принимает api ключ для api ресурса с информацией о ценных бумагах, и список акций пользователя,
    и возвращает словарь с информацией об указанных акциях"""

    logger.info("Запущена функция external_api_stock_prices")

    stock_dicts_list = []
    for stock in stock_list:
        url = f"https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={stock}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                stock_dicts_list.append({"stock": stock, "price": response.json()["data"][0]["mark"]})
            except KeyError:
                logger.error(f"Ошибка получения JSON ответа от апи: {response.json()}")
                return []

    logger.info("Ответ от стороннего апи акций получен. Код ответа - 200. Успешно.")
    logger.info("Функция external_api_stock_prices успешно вернула JSON ответ")

    url = f"https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol='APPL'&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:

        logger.error(
            f"Ответ от стороннего апи акций неуспешный. Код ответа - {response.status_code}."
            f"Ошибка получения JSON ответа."
        )

    return stock_dicts_list


def get_user_stocks(path_to_user_json):
    """Функция принимает путь до файла с данными пользователя о валютах и акциях
    и возвращает список акций пользователя"""

    logger.info("Запущена функция get_user_stocks")

    try:
        with open(path_to_user_json, "r") as user_settings_json:
            data = json.load(user_settings_json)
            stock_list = data[0]["user_stocks"]

            logger.info("Функция get_user_stocks успешно вернула список акций пользователя")

            return stock_list

    except FileNotFoundError as ex:

        logger.error(f"Ошибка функции get_user_stocks: {ex}")

        return []


def get_user_currencies(path_to_user_json):
    """Функция принимает путь до файла с данными пользователя о валютах и акциях
    и возвращает список валют пользователя"""

    logger.info("Запущена функция get_user_currencies")

    try:
        with open(path_to_user_json, "r") as user_settings_json:
            data = json.load(user_settings_json)
            currencies_list = data[0]["user_currencies"]

            logger.info("Функция get_user_currencies успешно вернула список валют пользователя")

            return currencies_list
    except FileNotFoundError as ex:

        logger.error(f"Ошибка функции get_user_currencies: {ex}")

        return []


def get_stocks_rates_json(stock_dicts_list):
    """Функция преобразовывет обновляет словарь с данными об акциях ключом stock_prices"""

    logger.info("Запущена функция get_stocks_rates_json")
    logger.info("Функция get_stocks_rates_json успешно вернула JSON ответ")

    return {"stock_prices": stock_dicts_list}


def get_currencies_rates_json(currency_list, currency_response_json):
    """Функция преобразовывает данные о валютах в номинал в рублях
    и вовзращает список с данными о валютах и их стоимости в рублях"""

    logger.info("Запущена функция get_currencies_rates_json")

    currencies = []
    for currency in currency_list:
        try:
            rub_currency_to_usd = currency_response_json["data"]["RUB"]
            currency_to_rub = 1 / currency_response_json["data"][currency] * rub_currency_to_usd
            currencies.append({"currency": currency, "rate": round(currency_to_rub, 2)})
        except TypeError:

            logger.error("Ошибка функции get_currencies_rates_json. Пустой ответ от апи")

            return []

    logger.info("Функция get_currencies_rates_json успешно вернула JSON ответ")

    return {"currency_rates": currencies}


def search_by_string(string, data):
    """Функция принимает строку для поиска информации в 'Категорях' и 'Описании',
    и возвращает JSON ответ с о всеми транзакциями в описании или категори которых найдена указанная строка
    """

    logger.info("Запущена функция search_by_string")

    pattern = re.compile(rf".*{string.lower()}.*")
    dict_info = []
    for i in range(len(data["Описание"])):
        match_1 = re.search(pattern, str(data["Категория"][i]).lower())
        match_2 = re.search(pattern, str(data["Описание"][i]).lower())
        dict_of_coincidences = {}
        if match_1 or match_2:
            for key in data.keys():
                dict_of_coincidences.update({key: data[f"{key}"][i]})
            dict_info.append(dict_of_coincidences)

    logger.info("Функция search_by_string успешно вернула JSON ответ")

    return dict_info
