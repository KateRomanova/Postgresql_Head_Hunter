import psycopg2
from get_vacancy import get_vacancies, get_companies
from config import config


def create_db(name, params):
    try:
        conn = psycopg2.connect(dbname='test', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {name}')
        cur.execute(f'CREATE DATABASE {name}')
        # conn.close()
        # cur.close()
        # conn = psycopg2.connect(dbname=name, **params)
        # cur = conn.cursor()
        # with conn.cursor() as cur:
        cur.execute(f'CREATE TABLE IF NOT EXISTS vacancies (company varchar (100), job_title varchar(100), '
                    f'link_to_vacancy varchar(100), salary_from int, salary_to int, description text, requirement text)')

        insert_query = ('INSERT INTO vacancies (company, job_title, link_to_vacancy, salary_from, salary_to,'
                        'description, requirement) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING')
        cur.executemany(insert_query, get_vacancies(get_companies()))
        conn.commit()
        cur.close()
        conn.close()

        print("Данные успешно вставлены в таблицу.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
