from src.reports import spending


class TestSpending:
    def test_spending(self, my_data):
        result = [
            {
                "Дата операции": "31.12.2021 19:55:55",
                "Категория": "Переводы",
                "Сумма операции": -13500,
            },
            {
                "Дата операции": "28.12.2021 18:30:30",
                "Категория": "Переводы",
                "Сумма операции": -169,
            },
        ]
        assert spending(my_data, "Переводы", "31.12.2021 23:30:30") == result

    def test_spending_now_time(self, my_data):
        result = []
        assert spending(my_data, "Переводы") == result

    def test_spending_category_not_found(self, my_data):
        result = []
        assert spending(my_data, "Шоколадки", "15.08.2021 15:08:20") == result

    def test_spending_no_categories_in_data_frame(self, my_data_without_categories):
        result = []
        assert spending(my_data_without_categories, "Супермаркеты", "13.04.2021 17:48:55") == result
