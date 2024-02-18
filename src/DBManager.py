import psycopg2

from utils.config import config

params = config()


class DBManager:
    """
    Класс для работы с базой данных
    """

    def __init__(self, database_name: str) -> None:
        self.database_name = database_name

    def execute_query(self, query: str) -> list[tuple]:
        """
        Возвращает результата выполнения запроса
        """
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """

        result = self.execute_query("SELECT company_name, vacancies_count FROM employers")
        return result

    def get_all_vacancies(self) -> list[tuple]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """

        result = self.execute_query("""
            SELECT employers.company_name, vacancy_name, salary_from, salary_to, url FROM vacancies
            JOIN employers USING (employer_id)
            """)
        return result

    def get_avg_salary(self) -> list[tuple]:
        """
        Получает среднюю зарплату по вакансиям
        """
        result = self.execute_query("SELECT AVG(salary_to) as avg_salary FROM vacancies")
        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        result = self.execute_query("""
            SELECT * FROM vacancies 
            WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)
            """)
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        result = self.execute_query(f"""
            SELECT * FROM vacancies 
            WHERE vacancy_name LIKE '%{keyword}%'
            """)
        return result
