import pandas as pd

from src.reports import spending
from src.services import search_by_string
from src.utils import get_transactions_data
from src.views import main_page_json_response

"""Запуск функции main_page_json_response"""

# if __name__ == "__main__":
#     print(main_page_json_response("ВАША ДАТА ЗДЕСЬ В ФОРМАТЕ ГГГГ.ММ.ДД ЧЧ:ММ:СС", 'operations.xls))

if __name__ == "__main__":
    print(main_page_json_response("2021.12.31 20:13:30", "operations.xls"))


"""Запуск функции spending"""

# if __name__ == "__main__":
#     data = pd.DataFrame(get_transactions_data('operations.xls))
#     result = spending(data, "ВАША КАТЕГОРИЯ", "ВАША ДАТА ЗДЕСЬ В ФОРМАТЕ ДД.ММ.ГГГГ ЧЧ:ММ:СС")
#     for operation in result:
#         print(operation)

if __name__ == "__main__":
    data = pd.DataFrame(get_transactions_data("operations.xls"))
    result = spending(data, "Переводы", "32.12.2021 23:30:30")
    for operation in result:
        print(operation)


"""Запуск функции search_by_string"""

# if __name__ == "__main__":
#     data = get_transactions_data('operations.xls)
#     result = search_by_string("ВАША СТРОКА ПОИСКА ЗДЕСЬ", data)
#     for operation in result:
#         print(operation)

if __name__ == "__main__":
    data = get_transactions_data("operations.xls")
    result = search_by_string("Перевод", data)
    for operation in result:
        print(operation)
