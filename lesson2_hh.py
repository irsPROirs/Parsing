from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


def salary_in_rubles(salary, n):
    vacancy_salary = []
    if salary[0:2] == 'от':
        vacancy_salary.append(float(salary.replace(' ', '')[2:]) * n)
        vacancy_salary.append('infinity')
    elif salary[0:2] == 'до':
        vacancy_salary.append(0)
        vacancy_salary.append(float(salary.replace(' ', '')[2:]) * n)
    else:
        a, b = salary.split('-')
        vacancy_salary.append(float(a) * n)
        vacancy_salary.append(float(b) * n)
    return vacancy_salary


# https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=Data+Science&page=0
main_link = 'https://hh.ru'
# vacancy_search = input('Введите название вакансии:')
vacancy_search = 'Data Science'
params = {'L_is_autosearch': 'false',
          'area': '1',
          'clusters': 'true',
          'enable_snippets': 'true',
          'text': vacancy_search,
          'page': 0}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
print(html.request.url)
soup = bs(html.text, 'html.parser')
final_page = int(soup.find('span', {'class': 'pager-item-not-in-short-range'}).find('a', {
    'class': 'bloko-button HH-Pager-Control'}).getText())
vacancies = []
for page in range(final_page + 1):
    params = {'L_is_autosearch': 'false',
              'area': '1',
              'clusters': 'true',
              'enable_snippets': 'true',
              'text': vacancy_search,
              'page': page}
    html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
    soup = bs(html.text, 'html.parser')

    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancies_list = vacancies_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_info = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
        vacancy_name = vacancy_info.getText()
        vacancy_link = vacancy_info['href']
        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary:
            salary = vacancy_salary.getText().replace('\xa0', '').replace(' ', '')
            if salary.find('руб.') > -1:
                salary = salary.replace('руб.', '')
                vacancy_salary = salary_in_rubles(salary, 1)
            if salary.find('USD') > -1:
                salary = salary.replace('USD', '')
                vacancy_salary = salary_in_rubles(salary, 70)
            if salary.find('EUR') > -1:
                salary = salary.replace('EUR', '')
                vacancy_salary = salary_in_rubles(salary, 90)

        employer_info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        employer_name = employer_info.getText()
        employer_link = main_link + employer_info['href']
        vacancy_data['emp_link'] = employer_link
        vacancy_data['emp_name'] = employer_name
        vacancy_data['salary'] = vacancy_salary
        vacancy_data['link'] = vacancy_link
        vacancy_data['name'] = vacancy_name
        vacancies.append(vacancy_data)
pprint(vacancies)
print(len(vacancies))
