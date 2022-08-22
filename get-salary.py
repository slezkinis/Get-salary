import requests
from pprint import pprint


def predict_rub_salary(salary):
    if salary == None:
        pass
    elif salary['currency'] != 'RUR':
        сalculated_salary = None
        return сalculated_salary
    elif salary['from'] and salary['to']:
        сalculated_salary = (salary['from'] + salary['to']) / 2
        return сalculated_salary
    elif not salary['to']:
        сalculated_salary = salary['from'] * 1.2
        return сalculated_salary
    else:
        сalculated_salary = salary['to'] * 0.8
        return сalculated_salary

        

if __name__ == '__main__':
    programming_jobs = {}
    popular_languages = [
        'JavaScript',
        'Java',
        'Ruby',
        'C++',
        'C#',
        'C',
        'Python',
        'Go'
    ]
    for language in popular_languages:
        about_profession = {}
        payload = {
            'text': f'Программист {language}', 
            'area': 1, 
            'period': 30
        }
        response = requests.get('https://api.hh.ru/vacancies/', params=payload)
        response.raise_for_status()
        vacancies = response.json()
        vacancies_amount = vacancies['found']
        payload = {
            'text': f'Программист {language}', 
            'area': 1, 
            'period': 30
        }
        vacancies_salaries = []
        response = requests.get('https://api.hh.ru/vacancies/', params=payload)
        response.raise_for_status()
        vacancies = response.json()['items']
        for vacancy in vacancies:
            vacancy_period_salary = vacancy['salary']
            vacancy_salary = predict_rub_salary(vacancy_period_salary)
            if vacancy_salary != None:
                vacancies_salaries.append(vacancy_salary)
        salaries_amount = 0
        for salary in vacancies_salaries:
            salaries_amount += salary
        vacancies_processed = len(vacancies_salaries)
        average_salary = salaries_amount / vacancies_processed
        # print(offesion['vacancies_found'] = vacancies_amount
        about_profession['average_salary'] = (average_salary)
        about_profession['vacancies_processed'] = vacancies_processed
        about_profession['average_salary'] = int(average_salary)
        programming_jobs[language] = about_profession
    pprint(programming_jobs)
