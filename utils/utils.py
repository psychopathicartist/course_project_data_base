import psycopg2

from src.HH_API import HeadHunterAPI
from utils.config import config

params = config()


def create_database(database_name: str):
    """
    Создание базы данных для сохранения данных о вакансиях
    """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()


def create_tables(database_name: str):
    """
    Создание таблиц в базе данных для сохранения данных о компаниях и их вакансиях
    """

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id VARCHAR(10) PRIMARY KEY,
                    company_name VARCHAR(50) NOT NULL,
                    vacancies_count INTEGER NOT NULL
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy_name VARCHAR(200) NOT NULL,
                    url VARCHAR NOT NULL,
                    salary_from INTEGER NOT NULL,
                    salary_to INTEGER NOT NULL,
                    employer_id VARCHAR(10) REFERENCES employers(employer_id)
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(database_name: str):
    """
    Сохранение данных о вакансиях и компаниях в базу данных
    """

    hh = HeadHunterAPI()
    employers = hh.get_employers_data()
    full_data = hh.get_full_data()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employers:
            cur.execute(
                """
                INSERT INTO employers VALUES (%s, %s, %s)
                """,
                (employer['id'], employer['name'], employer['vacancies_count'])
            )
        for company in full_data.values():
            for vacancy in company:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_name, url, salary_from, salary_to, employer_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy['name'], vacancy['url'], vacancy['salary_from'],
                     vacancy['salary_to'], vacancy['employer_id'])
                )

    conn.commit()
    conn.close()
