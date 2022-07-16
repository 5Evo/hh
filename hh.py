'''
программа для поиска резюме на HH.RU по клюевым словам
и анализа профессиональных требований к соискателю
'''

import requests
from save_files import save_data
from hh_methods import calculate_salary
from hh_methods import skil_stat

# Блок констант
DOMAIN = 'https://api.hh.ru/'


# проверка на доступность сервера
def hh_is_ok(url=DOMAIN):
    result = requests.get(url)
    print('Сервер отвечает, все ОК') if result.status_code == 200 else print(result.status_code)




# для начала проверим доступность сервера
hh_is_ok()


# Запросим критерии поиска вакансии:
search = 'python developer'     # поисковый запрос

# page = 15                    # номер запрашиваемой страницы
# params = {
#         'text': search,
#         'page': page,       # есть страницы т.к. данных много
#         }


# запроcим все вакансии по нашим критериям
request_skils = []      # список навыков по всем вакансиям
request_sallary = []    # список зарплат по всем вакансиям
all_id = []             # спиоск id всех найденный вакансий

url_vacancies = f'{DOMAIN}vacancies'
per_page = 30

while True: # запросим колчисвто страниц
    try:
        pages = int(input(f'На странице будет {per_page} вакансий. Сколько страниц (максимум {2000/per_page}): '))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")

for page in range(pages):  # API Отдает максимум 2000 вакансий (20 страниц по 100 вакансий)
    params = {
            'text': search,
            'page': page,       # есть страницы т.к. данных много
            'per_page': per_page
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
         #print(f'------------- вакансия {vacancy}')
         # id_temp = vacancies['items'][vacancy]['id']
         all_id.append(vacancies['items'][vacancy]['id']) #
    # TODO: проверить на наличие скилов: их может и не быть и выдаст следующую ошибку:
    # Traceback (most recent call last):
    # File "C:\Users\aleks\PycharmProjects\hh\hh.py", line 69, in <module>
    # vacancy_skils = requests.get(url_vacancy).json()['key_skills']
    # KeyError: 'key_skills'

    # разберем навыки и доход внутри каждой вакансии:
    for vacancy in range(per_page):         # пробежимся по первым 100 вакансиям
        url_vacancy = vacancies['items'][vacancy]['url']        # получим ссылку на вакансию
        #print(f'Страница {page}. Вакансия {vacancy}: {url_vacancy}')

        # обрабатываем скилы:
        try:
            vacancy_skils = requests.get(url_vacancy).json()['key_skills']
        except Exception as e:
            print('Не могу плучить данные по вакансии')
            vacancy_skils = {'name': None}
            print('в Скилы сохранили None ')

        for skil in vacancy_skils:          # добавим скилы текущей вакансии в общий список скилов:
            try:
                request_skils.append(skil['name'])
            except Exception as e:
                print('Не получилось выбрать Скил')

        #обрабатываем зарплаты:
        try:
            vacancy_salary = requests.get(url_vacancy).json()['salary']
            request_sallary.append(vacancy_salary)
        except Exception as e:
            print('Не указан доход')

        print(f'Требуемые скилы: {vacancy_skils}')
        print(f'Доход: {vacancy_salary}')




print(f'Обработали все страницы, количество найденых ID {len(all_id)}')
#print(f'Полный список навыков для всех вакансий: {request_skils}')
av_salary = calculate_salary(request_sallary)
print(f'Доходы по всем вакансиям: {av_salary}')
skil_report = skil_stat(request_skils)
print(f'статистика по скилам: {skil_report}')

save_data('competencies.txt', skil_report)
save_data('salary.txt', av_salary)