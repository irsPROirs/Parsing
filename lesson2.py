from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

# https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&text=data+science&showClusters=false
main_link = 'https://hh.ru'
# vacancy = input('Введите название вакансии:').replace(' ', '+')
vacancy = 'Data Science'
params = {'area': '1',
          'clusters': 'true',
          'enable_snippets': 'true',
          'text': vacancy,
          'showClusters': 'false'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
pprint(html.text)
# soup = bs(html.text, 'html.parser')
#
# vacancies_block = soup.find('div', {'data-qa': 'vacancy-serp__results'})
# vacancies_list = vacancies_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
# vacancies = []
# for vacancy in vacancies_list:
#     vacancy_data = {}
#     vacancy_info = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
#     vacancy_link = vacancy_info.parent['href']
#     pprint(vacancy_info)
    # serial_name = serial_info.getText()
    # serial_genre = serial.find('span',
    #                            {'class': 'selection-film-item-meta__meta-additional-item'}).nextSibling.getText()
    # serial_rating = serial.find('span', {'class': 'rating__value'})
    # if serial_rating:
    #     serial_rating = serial_rating.getText()
    #     try:
#             serial_rating = float(serial_rating)
#         except:
#             pass
#
#     serial_data['name'] = serial_name
#     serial_data['link'] = serial_link
#     serial_data['genre'] = serial_genre
#     serial_data['rating'] = serial_rating
#
#     serials.append(serial_data)
#
# pprint(vacancies)
