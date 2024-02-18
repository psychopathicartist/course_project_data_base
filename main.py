from src.DBManager import DBManager
from utils.utils import *


def user_interaction(database_name: str) -> None:
    """
    Функция ля взаимодействия с пользователем
    """
    create_database(database_name)
    create_tables(database_name)
    save_data_to_database(database_name)
    user_db_manager = DBManager(database_name)
    print("""Выберите запрос:
    1 - Получить список всех компаний и количество открытых вакансий у каждой компании
    2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    3 - Получить среднюю зарплату по вакансиям
    4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5 - Получить список всех вакансий, в названии которых содержится ключевое слово
    6 - Завершить работу с базой данных
        """)
    while True:
        user_choice = input()
        if user_choice == '1':
            result = user_db_manager.get_companies_and_vacancies_count()
            for company in result:
                print(company)
                print('*' * 50)
        elif user_choice == '2':
            result = user_db_manager.get_all_vacancies()
            for vacancy in result:
                print(vacancy)
                print('*' * 100)
        elif user_choice == '3':
            result = user_db_manager.get_avg_salary()
            print(round(result[0][0]))
        elif user_choice == '4':
            result = user_db_manager.get_vacancies_with_higher_salary()
            for vacancy in result:
                print(vacancy)
                print('*' * 100)
        elif user_choice == '5':
            user_keyword = input('Введите ключевое слово: ')
            result = user_db_manager.get_vacancies_with_keyword(user_keyword.title())
            if result:
                for vacancy in result:
                    print(vacancy)
                    print('*' * 100)
            else:
                print('Результатов по данному запросу не найдено')
        elif user_choice == '6':
            break
        else:
            print('Неверный ввод')


if __name__ == '__main__':
    db_name = input('Введите название базы данных для сохранения результатов: ')
    user_interaction(db_name)
