import requests
import bs4
import fake_headers
import json


hh_url = 'https://spb.hh.ru/search/vacancy?text=python%2C+django%2C+flask&area=1&area=2'
vacancy_data = []


def vacancy_finder():
    for page in range(0, 5):
        headers_gen = fake_headers.Headers(os='win', browser='chrome')
        response = requests.get(f'{hh_url}&page={page}', headers=headers_gen.generate()).text
        main_page = bs4.BeautifulSoup(response, 'lxml')
        link_main = main_page.find_all('div', class_='serp-item')
        for tag in link_main:
            header = tag.find('a').text.strip()
            link = tag.find('a')['href']
            salary_chek = tag.find('span', attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
            company = tag.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.replace('\xa0', ' ')
            city = tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
            if salary_chek is None:
                vacancy_data.append({'Вакансия': header,
                                     'Ссылка': link,
                                     'Зарплата': 'Зарплата не указана',
                                     'Компания': company,
                                     'Город': city
                                     })
            else:
                salary = salary_chek.text.replace('\u202f', '')
                vacancy_data.append({'Вакансия': header,
                                     'Ссылка': link,
                                     'Зарплата': salary,
                                     'Компания': company,
                                     'Город': city
                                     })

    return vacancy_data


def data_to_json():
    vacancy_dict = vacancy_finder()
    with open('Vacancies.json', 'w') as file:
        json.dump(vacancy_dict, file)


if __name__ == '__main__':
    data_to_json()
