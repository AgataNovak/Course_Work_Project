import datetime
import os

import pandas as pd

from src.logger import setup_logger
from src.utils import get_transactions_data

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_logs = os.path.join(current_dir, "../logs", "reports.log")
logger = setup_logger("reports", file_path_logs)


def spending(data, category, date=datetime.datetime.now()):
    """Функция принимает DataFrame с транзакциями, название категории и дату,
    и возвращает траты по заданной категории за последние три месяца от переданной даты.
    По умолчанию дата принимается сегодняшним числом на момент запуска функции"""

    logger.info("Запущена функция spending")

    data_dict = data.to_dict()
    result = []
    type_date = type(date)
    if type_date == datetime.datetime:
        current_date_obj = date
    else:
        try:
            current_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        except ValueError:
            return []

    try:
        for i in range(len(data_dict["Дата операции"])):
            if data_dict["Категория"][i] == category:
                date_ = data_dict["Дата операции"][i]
                date_obj = datetime.datetime.strptime(str(date_), "%d.%m.%Y %H:%M:%S")
                if current_date_obj.month in [4, 5, 6, 7, 8, 9, 10, 11, 12]:
                    if current_date_obj.day == 31:
                        limit_day = current_date_obj.replace(
                            month=(current_date_obj.month - 3),
                            day=(current_date_obj.day - 1),
                        )
                    else:
                        limit_day = current_date_obj.replace(month=(current_date_obj.month - 3))
                else:
                    if current_date_obj.month == 2:
                        limit_day = current_date_obj.replace(
                            year=(current_date_obj.year - 1),
                            month=(current_date_obj.month + 9),
                            day=(current_date_obj.day + 2),
                        )
                    else:
                        if current_date_obj.day == 31:
                            limit_day = current_date_obj.replace(
                                year=(current_date_obj.year - 1),
                                month=(current_date_obj.month + 9),
                                day=(current_date_obj.day - 1),
                            )
                        else:
                            limit_day = current_date_obj.replace(
                                year=current_date_obj.year - 1,
                                month=current_date_obj.month + 9,
                            )

                if limit_day <= date_obj:
                    if date_obj <= current_date_obj:
                        if data_dict["Сумма операции"][i] < 0:
                            result.append(
                                {
                                    "Категория": data_dict["Категория"][i],
                                    "Сумма операции": data_dict["Сумма операции"][i],
                                    "Дата операции": data_dict["Дата операции"][i],
                                }
                            )

        logger.info("Функция spending успешно вернула список с отфильтрованными транзакциями")

        return result
    except KeyError as ex:

        logger.error(f"Ошибка функции spending: {ex}")

        return []


if __name__ == "__main__":
    data = pd.DataFrame(get_transactions_data("operations.xls"))
    result = spending(data, "Переводы", "32.12.2021 23:30:30")
    for operation in result:
        print(operation)
