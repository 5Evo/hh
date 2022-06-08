'''
программа для поиска резюме на HH.RU по клюевым словам
и анализа профессиональных требований к соискателю
'''

import requests
import json
from pprint import pprint

from hh_methods import skil_stat

# Блок констант
DOMAIN = 'https://api.hh.ru/'


# проверка на доступность сервера
def hh_is_ok(url=DOMAIN):
    result = requests.get(url)
    print('Сервер отвечает, все ОК') if result.status_code == 200 else print(result.status_code)




# для начала проверим доступность сервера
# hh_is_ok()


# Запросим критерии поиска вакансии:
search = 'python developer'     # поисковый запрос

# page = 15                    # номер запрашиваемой страницы
# params = {
#         'text': search,
#         'page': page,       # есть страницы т.к. данных много
#         }


# запроcим все вакансии по нашим критериям
request_skils = [] # подготовим список навыков по всем вакансиям
all_id = []
url_vacancies = f'{DOMAIN}vacancies'
for page in range(20):
    params = {
            'text': search,
            'page': page,       # есть страницы т.к. данных много
            'per_page': 100
            }
    print(f' Получаем страницу {page}')
    vacancies = requests.get(url_vacancies, params=params).json()
    vacancy_count = vacancies['found']          # сколько всего вакансий нашли
    page_count = vacancies['pages']             # сколько страниц с вакансиями
    per_page = vacancies['per_page']
    #print(f'Поиск по "{search}" \nНайдено вакансий: {vacancy_count} на {page_count} страницах')
    #pprint(vacancies)
    # составим список ID всех вакансий на странице:
    for vacancy in range(per_page):
         print(f'------------- вакансия {vacancy}')
         id_temp = vacancies['items'][vacancy]['id']
         all_id.append(id_temp)
    # TODO: проверить на наличие скилов: их может и не быть и выдаст следующую ошибку:
    # Traceback (most recent call last):
    # File "C:\Users\aleks\PycharmProjects\hh\hh.py", line 69, in <module>
    # vacancy_skils = requests.get(url_vacancy).json()['key_skills']
    # KeyError: 'key_skills'

    # разберем навыки внутри каждой вакансии:
    for vacancy in range(per_page):         # пробежимся по первым 100 вакансиям

        # получим ссылку на вакансию
        url_vacancy = vacancies['items'][vacancy]['url']
        print(f'Страница {page}. Вакансия {vacancy}: {url_vacancy}')

        # из отдельного запроса по вакансии получить необходимые данные
        #TODO: Если нет скилов в первой вакансии - ошибка
        try:
            vacancy_skils = requests.get(url_vacancy).json()['key_skills']
            vacancy_salary = requests.get(url_vacancy).json()['salary']
        except Exception as e:
            print('Не могу плучить данные по вакансии')

        # добавим скилы текущей вакансии в общий список скилов:
        for skil in vacancy_skils:
            request_skils.append(skil['name'])

        print(f'Требуемые скилы: {vacancy_skils}')
        print(f'Доход: {vacancy_salary}')
        # собрать все данные в свой список



                    # получение данных со страницы вакансии

                    #items_num = 1       # какую запись (вакансию) просмотрим
                    #key_params = 'id'   # что именно внутри вакансии интересует
                    #print('ID вакансии:', vacancies['items'][items_num][key_params])
                    # pprint(vacancies['items'][items_num]) # выводим информацию о вакансии из общего списка вакансий
                    # pprint(vacancies)
                    # пройдемся по  всем вакансиям и сохраним краткую выжимку по вакансиям в список

print(f'Обработали все страницы, количество найденых ID {len(all_id)}')




# for vacancy in range(100):         # пробежимся по первым 100 вакансиям
#
#     # получим ссылку на вакансию
#     url_vacancy = vacancies['items'][vacancy]['url']
#     print(f'Вакансия {vacancy}: {url_vacancy}')
#
#     # из отдельного запроса по вакансии получить необходимые данные
#     vacancy_skils = requests.get(url_vacancy).json()['key_skills']
#     vacancy_salary = requests.get(url_vacancy).json()['salary']
#
#     # добавим скилы текущей вакансии в общий список скилов:
#     for skil in vacancy_skils:
#         request_skils.append(skil['name'])
#
#     print(f'Требуемые скилы: {vacancy_skils}')
#     print(f'Доход: {vacancy_salary}')
#     # собрать все данные в свой список
#
#
# print(f'Полный список навыков для всех вакансий: {request_skils}')
skil_report = skil_stat(request_skils)
print(f'статистика по скилам: {skil_report}')