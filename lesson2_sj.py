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
    elif salary.find('-') > -1:
        a, b = salary.split('-')
        vacancy_salary.append(float(a) * n)
        vacancy_salary.append(float(b) * n)
    else:
        vacancy_salary.append(None)
        vacancy_salary.append(None)
    return vacancy_salary


# https://www.superjob.ru/vacancy/search/?keywords=%D0%A3%D0%B1%D0%BE%D1%80%D1%89%D0%B8%D1%86%D0%B0%20%D0%BF%D0%BE%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D0%B9&geo%5Bt%5D%5B0%5D=4
main_link = 'https://www.superjob.ru'
# vacancy_search = input('Введите название вакансии:')
vacancy_search = 'Уборщица помещений'
params = {'keywords': vacancy_search,
          'geo[t][0]': '4',
          'page': 1}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
html = requests.get(main_link + '/vacancy/search/', params=params, headers=headers)
print(html.request.url)
soup = bs(html.text, 'html.parser')
f_page = soup.find_all('a', {'class': '_3ze9n'})
final_page = int(f_page[len(f_page) - 2].getText())
vacancies = []
for page in range(1, final_page + 1):
    params = {'keywords': vacancy_search,
              'geo[t][0]': '4',
              'page': page}
    html = requests.get(main_link + '/vacancy/search/', params=params, headers=headers)
    soup = bs(html.text, 'html.parser')
    vacancies_block = soup.find('div', {'class': '_1ID8B'})
    vacancies_list = vacancies_block.find_all('div', {'class': 'f-test-vacancy-item'})
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_info = vacancy.find('a')
        vacancy_name = vacancy_info.getText()
        vacancy_link = main_link + vacancy_info['href']
        vacancy_salary = vacancy.find('span', {'class': '_3mfro'})
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

        vacancy_data['salary'] = vacancy_salary
        vacancy_data['link'] = vacancy_link
        vacancy_data['name'] = vacancy_name
        vacancies.append(vacancy_data)
pprint(vacancies)
