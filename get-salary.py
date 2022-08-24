import os

import requests
from terminaltables import DoubleTable
from dotenv import load_dotenv


POPULAR_LANGUAGES = [
    'JavaScript',
    'Java',
    'Ruby',
    'C++',
    'C#',
    'C',
    'Python',
    'Go',
    '1c'
]


def predict_rub_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return
    elif salary_from and salary_to:
        сalculated_salary = (salary_from + salary_to) / 2
        return сalculated_salary
    elif not salary_to or salary_to == 0:
        сalculated_salary = salary_from * 1.2
        return сalculated_salary
    else:
        сalculated_salary = salary_to * 0.8
        return сalculated_salary


def print_table(vacancies_data, title):
    languages = [language for language in vacancies_data]
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    for language in languages:
        about_language = [
            language,
            vacancies_data[language]['vacancy_amount'],
            vacancies_data[language]['vacancies_processed'],
            vacancies_data[language]['average_salary']
        ]
        table_data.append(about_language)
    table_instance = DoubleTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()


def predict_rub_salary_hh():
    programming_jobs_hh = {}
    for language in POPULAR_LANGUAGES:
        about_vacancy = {}
        payload = {
            'text': f'Программист {language}',
            'area': 1,
            'period': 30
        }
        response = requests.get('https://api.hh.ru/vacancies/', params=payload)
        response.raise_for_status()
        vacancies = response.json()['items']
        vacancies_amount = response.json()['found']
        vacancies_salaries = []
        vacancies_processed = 0
        for vacancy in vacancies:
            vacancy_period_salary = vacancy['salary']
            if vacancy_period_salary:
                if vacancy_period_salary['currency'] == 'RUR':
                    vacancy_salary = predict_rub_salary(
                        vacancy_period_salary['from'],
                        vacancy_period_salary['to'],
                        vacancy_period_salary['currency']
                        )
                    if vacancy_salary:
                        vacancies_salaries.append(vacancy_salary)
        salaries_amount = 0
        for salary in vacancies_salaries:
            salaries_amount += salary
        vacancies_processed = len(vacancies_salaries)
        average_salary = salaries_amount / vacancies_processed
        about_vacancy['vacancy_amount'] = vacancies_amount
        about_vacancy['vacancies_processed'] = vacancies_processed
        about_vacancy['average_salary'] = int(average_salary)
        programming_jobs_hh[language] = about_vacancy
    return programming_jobs_hh


def predict_rub_salary_sj(sj_token):
    programming_jobs_sj = {}
    for language in POPULAR_LANGUAGES:
        vacancies_salaries = []
        vacancies_processed = 0
        about_vacancy = {}
        number_page = 0
        vacancy_amount = 0
        more_pages = True
        while more_pages:
            headers = {
                'X-Api-App-Id': sj_token
            }
            payload = {
                'town': 4,
                'catalogues': 48,
                'page': number_page,
                'count': 100,
                'keyword': language
            }
            response = requests.get(
                'https://api.superjob.ru/3.0/vacancies',
                headers=headers,
                params=payload
                )
            response.raise_for_status()
            page = response.json()
            for about_vacancy in page['objects']:
                if about_vacancy['currency'] == 'rub':
                    vacancy_salary = predict_rub_salary(
                        about_vacancy['payment_from'],
                        about_vacancy['payment_to'],
                        about_vacancy['currency']
                    )
                if vacancy_salary:
                    vacancies_salaries.append(vacancy_salary)
                    vacancies_processed += 1
            number_page += 1
            vacancy_amount += page['total']
            more_pages = page['more']
        salaries_amount = 0
        for salary in vacancies_salaries:
            salaries_amount += salary
        vacancies_processed = len(vacancies_salaries)
        average_salary = salaries_amount / vacancies_processed
        about_vacancy['vacancy_amount'] = vacancy_amount
        about_vacancy['vacancies_processed'] = vacancies_processed
        about_vacancy['average_salary'] = int(average_salary)
        programming_jobs_sj[language] = about_vacancy
    return programming_jobs_sj


if __name__ == '__main__':
    load_dotenv()
    sj_token = os.environ['SJ_TOKEN']
    print_table(predict_rub_salary_hh(), 'HeadHunter Moscow')
    print_table(predict_rub_salary_sj(sj_token), 'SuperJob Moscow')
