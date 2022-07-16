import statistics

def skil_stat(skils):
    '''
    считаем статистику по скилам всех вакансий:
    на входе принимаем полный список скилов всех вакансий
    на выходе - формируем словарь: 'скил': количество скила во всех вакансиях
    :param skils: список скилов всех вакансий
    :return: сортированный словарь 'скил': количество скила во всех вакансиях
    '''
    # Сделаем из Списка скилов Множество скилов (уберем повторы) и приведем к нижнему регистру:
    skils_lower = [skil.lower() for skil in skils]      # приведем все к ниижнему регистру
    skils_set = set(skils_lower)

    # Сгенерируем словарь с количеством повторов каждого скила:
    skils_stat = {item: skils_lower.count(item) for item in skils_set}

    # отсортируем словарь по значениям:
    sorted_tuple = sorted(skils_stat.items(), key=lambda x: x[1], reverse=True) # отсориторвали все элементы словаря по значению
    skils = dict(sorted_tuple)

    return skils

def calculate_salary(income):
    '''
    Считаем статистику по зарплатам:
    на входе принимаем все з/пл, делим их на рублевые и долларовые, затем
    берем среднее значение по нижней гранце и отдельно среднее значение
    по верхней границе для каждой валюты
    :param income:
    :return:
    '''

    count = 0
    from_rub = []
    from_usd = []
    to_rub = []
    to_usd = []
    for item in income:
        count += 1
        if item == None:
            pass
            # print(f'{count}. - None -')
        else:
            # print(f'{count}. {type(item)} {item}')
            match item['currency']:
                case 'RUR':
                    #print(f'{count}. ')
                    try:
                        from_temp = item['from']
                        #print(f'мин RUR: {from_temp}')
                        if item['from'] != None:
                            from_rub.append(item['from'])
                        else:
                            pass
                    except:
                        print('нет from для рублей')

                    try:
                        to_temp = item['to']
                        #print(f'макс RUR: {to_temp}')
                        if item['to'] != None:
                            to_rub.append(item['to'])
                        else:
                            pass
                    except:
                        print('нет to для рублей')

                case 'USD':
                    print(f'{count}. ')
                    try:
                        from_temp = item['from']
                        #print(f'мин USD: {from_temp}')
                        if item['from'] != None:
                            from_usd.append(item['from'])
                        else:
                            pass
                    except:
                        print('нет from для $')
                    try:
                        to_temp = item['to']
                        #print(f'макс USD: {to_temp}')
                        if item['to'] != None:
                            to_usd.append(item['to'])
                        else:
                            pass
                    except:
                        print('нет to для USD')
                case None:
                    pass

    # закончили разбор на компонетнты, проверим что имеем:
    av_min_ru = statistics.mean(from_rub)
    av_min_usd = statistics.mean(from_usd)
    av_max_ru = statistics.mean(to_rub)
    av_max_usd = statistics.mean(to_usd)

    print(f'Мин Руб: {av_min_ru} - {from_rub}')
    print(f'Мин USD: {av_min_usd} - {from_usd}')
    print(f'Макс Руб: {av_max_ru} - {to_rub}')
    print(f'Макс USD: {av_max_usd} - {to_usd}')
    return {'Avarega slary, RUR':
                {'from': av_min_ru, 'to': av_max_ru},
            'Avarega slary, USD':
                {'from': av_min_usd, 'to': av_max_usd}
            }

if __name__=='__main__':
    test = [None, {'from': 150000, 'to': 250000, 'currency': 'RUR', 'gross': False}, {'from': None, 'to': 300000, 'currency': 'RUR', 'gross': False}, {'from': None, 'to': 270000, 'currency': 'RUR', 'gross': False}, {'from': None, 'to': 270000, 'currency': 'RUR', 'gross': False}, None, None, {'from': 2500, 'to': None, 'currency': 'USD', 'gross': False}, None, None, None, {'from': 300000, 'to': 360000, 'currency': 'RUR', 'gross': False}, None, None, None, {'from': 100000, 'to': 250000, 'currency': 'RUR', 'gross': False}, None, {'from': 900000, 'to': 1200000, 'currency': 'KZT', 'gross': True}, {'from': 200000, 'to': None, 'currency': 'RUR', 'gross': False}, None, None, None, {'from': None, 'to': 220000, 'currency': 'RUR', 'gross': True}, None, None, None, {'from': 120000, 'to': 220000, 'currency': 'RUR', 'gross': False}, {'from': 350000, 'to': 400000, 'currency': 'RUR', 'gross': False}, {'from': 1500, 'to': 3500, 'currency': 'USD', 'gross': False}, None]
    av_salary = calculate_salary(test)
    print(f'В результате: {av_salary}')