import os
import re

from src.logger import setup_logger
from src.utils import get_transactions_data

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_logs = os.path.join(current_dir, "../logs", "services.log")
logger = setup_logger("services", file_path_logs)


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

    logger.info(
        "Функция search_by_string успешно вернула список отфильрованных транзакций"
    )

    return dict_info


if __name__ == "__main__":
    data = get_transactions_data()
    result = search_by_string("Перевод", data)
    for operation in result:
        print(operation)
