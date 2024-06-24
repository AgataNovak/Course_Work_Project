from src.services import search_by_string


class TestSearchByString:

    def test_search_by_string(self, my_data_dict):

        result = [
            {
                "Дата операции": "15.12.2021 07:35:15",
                "Дата платежа": "15.12.2021",
                "Категория": "Пополнения",
                "Номер карты": "*0003",
                "Описание": "Пополнение через Газпромбанк",
                "Статус": "CANCELED",
                "Сумма операции": 5000,
                "Сумма операции с округлением": 5000,
            }
        ]
        assert search_by_string("Газпром", my_data_dict) == result

    def test_search_by_string_nothing_found(self, my_data_dict):

        result = []
        assert search_by_string("Example", my_data_dict) == result
