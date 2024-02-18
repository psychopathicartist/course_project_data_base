import requests


class HeadHunterAPI:
    """
    Класс для работы с API сайта hh.ru
    """

    @staticmethod
    def get_employers_request() -> list[dict]:
        """
        Возвращает список из 10 работодателей с открытыми вакансиями
        """

        hh_api_url = 'https://api.hh.ru/employers'
        params = {
            'only_with_vacancies': True,
            'sort_by': 'by_vacancies_open',
            'per_page': 10
        }
        response = requests.get(hh_api_url, params=params).json()
        return response['items']

    def get_employers_data(self) -> list[dict]:
        """
        Возвращает список работодателей, полученных в методе get_employers_request,
        в котором содержатся лишь указанные поля: id, название компании, количество вакансий
        """

        employers_data = []
        employers = self.get_employers_request()
        for employer in employers:
            employer_data = {
                'id': employer['id'],
                'name': employer['name'],
                'vacancies_count': employer['open_vacancies']
            }
            employers_data.append(employer_data)
        return employers_data

    @staticmethod
    def get_vacancies_request(employer_id: str) -> list[dict]:
        """
        Возвращает список из 20 вакансий для каждой компании
        """

        hh_api_url = 'https://api.hh.ru/vacancies'
        params = {
            'per_page': 20,
            'employer_id': employer_id,
            'only_with_salary': True
        }

        response = requests.get(hh_api_url, params=params).json()
        return response['items']

    def get_vacancies_data(self, employer_id: str) -> list[dict]:
        """
        Возвращает список вакансий, полученных в методе get_vacancies_request,
        в котором содержатся лишь указанные поля:
        название, ссылка, зарплата от, зарплата до, id компании
        """

        vacancies_data = []
        vacancies = self.get_vacancies_request(employer_id)
        for vacancy in vacancies:
            vacancy_data = {
                'name': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': int(vacancy['salary']['to'] / 2) if vacancy['salary']['from'] is None
                else vacancy['salary']['from'],
                'salary_to': vacancy['salary']['from'] if vacancy['salary']['to'] is None
                else vacancy['salary']['to'],
                'employer_id': employer_id
            }
            vacancies_data.append(vacancy_data)
        return vacancies_data

    def get_full_data(self) -> dict[list]:
        """
        Возвращает словарь из полученных данных, содержащий название компании как ключ
        и список данных о вакансиях этой компании как значение
        """

        full_data = {}
        employers = self.get_employers_data()
        for employer in employers:
            full_data[employer['name']] = []
            vacancies = self.get_vacancies_data(employer['id'])
            for vacancy in vacancies:
                full_data[employer['name']].append(vacancy)
        return full_data
