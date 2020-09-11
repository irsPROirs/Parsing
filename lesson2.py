from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'https://hh.ru/search/vacancy?enable_snippets=true&no_magic=true&text='
vacancy = input('Введите название вакансии:').replace(' ', '+')

params = {'area': '1',
          'clusters': 'true',
          'enable_snippets': 'true',
          'no_magic': 'true',
          'text': vacancy}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)

soup = bs(html.text, 'html.parser')

vacancies_block = soup.find('div', {'class': 'bloko-gap bloko-gap_s-top bloko-gap_m-top bloko-gap_l-top'})
vacancies_list = vacancies_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

serials = []
for serial in serials_list:
    serial_data = {}
    serial_info = serial.find('p')
    serial_link = main_link + serial_info.parent['href']
    serial_name = serial_info.getText()
    serial_genre = serial.find('span',
                               {'class': 'selection-film-item-meta__meta-additional-item'}).nextSibling.getText()
    serial_rating = serial.find('span', {'class': 'rating__value'})
    if serial_rating:
        serial_rating = serial_rating.getText()
        try:
            serial_rating = float(serial_rating)
        except:
            pass

    serial_data['name'] = serial_name
    serial_data['link'] = serial_link
    serial_data['genre'] = serial_genre
    serial_data['rating'] = serial_rating

    serials.append(serial_data)

pprint(serials)
