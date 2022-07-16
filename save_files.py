'''
1. открыть файл на запись
2. записать обработанные данные
3. закрыть файйл
4. реализовать через try и исключения

competencies.txt - файл с ключевыми компетенциями
salary.txt - файл с доходами

'''
import json


def save_data(file_name, data):
    '''
    :param file_name: имя записываемого файла
    :param data: записываемые текстовые данные
    :return:
    '''
    try:
        f = open(file_name, 'w')
        data_json = json.dumps(data)
        f.write(data_json)
        f.close()
    except Exception as e:
        print(f'ошибка записи: {e}')

if __name__ == "__main__":
    data_to_write = [{'name': 'Linux'}, {'name': 'Python'}, {'name': 'Docker'}, {'name': 'Kubernetes'}, {'name': 'Умение принимать решения'}]
    save_data('competencies.txt', data_to_write)