# Cuorse Work by Agata Gorskaia

## Описание
Эта программа - курсовая работа, созданный для разработки виджета взаимодействия пользователя с личным кабинетом банка.
Виджет содержит следующие функции:

+ ***модуль views.py*** :
Основная функция "main_page_json_response" находится в модуле "views.py".
Это интерактивная функция, принимающая дату и возвращающая JSON ответ с приветствием и основной информацией о картах и операциях клиента банка.

+ ***модуль utils.py*** :
Содержит функции обрабатывающие excel таблицу с данными о транзакциях.
Функции модуля utils используются в функции main_page_json_respnose.

+ ***модуль services.py*** :
Содержит функцию search_by_string, обеспечивающую поиск транзакций с введённой строкой в описании ил категории транзакции.

+ ***модуль reports.py*** :
Содержит функцию spending, обеспечивающую вывод списка трат за три последние месяца от введённой даты.  


## Установка: 

Клонируйте репозиторий:
https://github.com/AgataNovak/Course_Work_Project


## Использование:
Задайте аргументы функциям в модулях:
1. views.py
2. services.py
3. reports.py
Excel файл с транзакциями должен находиться в директории data
user_settings.json файл должен находиться в директории data


## Тестирование:
Тесты программы заданы и пройдены, ознакомиться с ними можно в директории "tests".
Тесты проведены по разным кейсам, соответствующим и несоответствующим условиям задания параметров виджета.
