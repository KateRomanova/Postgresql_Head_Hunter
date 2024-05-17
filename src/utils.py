import psycopg2
import json

def create_db(name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {name}')
    cur.execute(f'CREATE DATABASE {name}')
    conn.close()
    conn = psycopg2.connect(dbname=name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    company varchar (100),
                    job_title varchar(100),
                    link_to_vacancy varchar(100),
                    salary_from int,
                    salary_to int,
                    description text,
                    requirement text); 
                    """)
    conn.commit()
    conn.close()


    with open('vacancy_json.json', 'r', encoding='utf-8') as file:  # заполняем таблицу данными из созданного json-файла
        vacancies = json.load(file)
        conn = psycopg2.connect(dbname=name, **params)
        for vacancy in vacancies:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO vacancies (company, job_title, link_to_vacancy, salary_from, salary_to, '
                    'description, requirement) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (vacancy.get('company'), vacancy.get('job_title'), vacancy.get('link_to_vacancy'),
                     vacancy.get('salary_from'), vacancy.get('salary_to'), vacancy.get('description'),
                     vacancy.get('requirement')))

        conn.commit()
        conn.close()
