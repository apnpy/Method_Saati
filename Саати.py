import numpy as np
import pandas as pd
from tabulate import tabulate

evaluations = {'Интенсивность относительной важности (в баллах)' : [1,3,5,7,9,"2, 4, 6, 8"],
        'Наименование' : ["Равная важность", "Слабое превосходство", "Сильное превосходство",
                                    "Очень сильное превосходство", "Очень сильное превосходство",
                                    "Абсолютное превосходство"]}

frame = pd.DataFrame(evaluations, index= [1,2,3,4,5,6])
print(frame)

# Количество критериев
number = 4
# Наименования критериев
names = ['Экологическая обстановка', "Развитие инфраструктуры", "Уровень дохода", "Стоимость недвижимости"]
names_up = ['Экологическая обстановка', "Развитие инфраструктуры", "Уровень дохода", "Стоимость недвижимости", "Результат-вектор весов"]

# Вывод критериев в таблице
krit = {'Критерии': names}
frame_krit = pd.DataFrame(krit, index = [1,2,3,4])
print(frame_krit)

# Функция для заполнения списка и вычисления вектора
def matrix(n,name):
    # Создаем матрицу: обращаемся к нумпаю, заполняем всю матрицу 1
    M = np.ones([n, n])
    for i in range(0, n):
        for j in range(0, n):
            # Пропуск единичных столбцов и столбцов под единичными
            if i < j:
                mij = float(input(f'\nНасколько критерий {i+1}  приоритетнее критерия {j+1}?\n'
                            'Введите коэффициент: '))
                M[i, j] = float(mij)
                M[j, i] = 1 / float(mij)  # Добавление обратных элементов (под главной диагональю)

    '''
    Чтобы вывести весовые коэффициенты, необходимо вычислить собственный вектор матрицы М.
    Для этого воспользуемся функцией numpy.linalg.eig(М)[1][:,0]
    '''
    vector = np.linalg.eig(M)[1][:, 0]
    c = vector.real
    # пронормируем вектор
    norm_vector = c / c.sum()
    norm_vector_glav = np.round(norm_vector, 4)
    data = []


    # Заполнение списка data
    for i in range(len(name)):
        data_add_list = []
        data_add_list.append(name[i])
        for j in range(len(M[i])):
            data_add_list.append(M[i][j])
        data.append(data_add_list)

    return norm_vector_glav, data

norm_vector_glav, data = matrix(number,names)

# Функция вывода результата
def result_vector(vect,datas,name):
    for x in range(len(vect)):
        df = pd.DataFrame(datas)
        df['Результат вектор весов'] = [x for x in vect]

    return print(tabulate(df, headers=name, tablefmt='fancy_grid', stralign='center'))

# Вывод таблицы с критериями
print(result_vector(norm_vector_glav,data,names_up))

##################################
# Наименования городов
city_names = ["Москва","Санкт-Петербург","Казань"]
city_names_up = ["Москва","Санкт-Петербург","Казань","Результат-вектор весов"]
city = 3

#Показатель «Экологическая обстановка»

print("\n\nПоказатель «Экологическая обстановка»\n")

# Таблица: наименования городов
city_tabl = {'Города:': city_names}
frame_сity = pd.DataFrame(city_tabl, index = [1,2,3,])
print(frame_сity)

norm_vector_eco, data_eco = matrix(city, city_names)
print(result_vector(norm_vector_eco,data_eco,city_names_up))

#Показатель «Развитие инфраструктуры»

print("\n\nПоказатель «Развитие инфраструктуры»")
norm_vector_infrastructure, data_infrastructure = matrix(city, city_names)

print(result_vector(norm_vector_infrastructure,data_infrastructure,city_names_up))

#Показатель «Уровень доходов»

print("\n\nПоказатель «Уровень доходов»")
norm_vector_cash, data_cash = matrix(city, city_names)
print(result_vector(norm_vector_cash,data_cash,city_names_up))

#Показатель «Стоимость недвижимости»

print("\n\nПоказатель «Стоимость недвижимости»")
norm_vector_realty, data_realty = matrix(city, city_names)
print(result_vector(norm_vector_realty,data_realty,city_names_up))

#############
# Перемножение веса показателя на вектор-результатов
eco_vector = []
for i in range(len(norm_vector_eco)):
        prom = norm_vector_eco[i] * norm_vector_glav[0]
        e = round(prom.real,4)
        eco_vector.append(e)

infrastructure_vector = []
for i in range(len(norm_vector_infrastructure)):
        prom1 = norm_vector_infrastructure[i] * norm_vector_glav[1]
        e1 = round(prom1.real,4)
        infrastructure_vector.append(e1)

cash_vector = []
for i in range(len(norm_vector_cash)):
        prom2 = norm_vector_cash[i] * norm_vector_glav[2]
        e2 = round(prom2.real,4)
        cash_vector.append(e2)

realty_vector = []
for i in range(len(norm_vector_realty)):
        prom3 = norm_vector_realty[i] * norm_vector_glav[3]
        e3 = round(prom3.real,4)
        realty_vector.append(e3)

# Расчет средневзвешенного
itog_vector = []
for k in range(len(eco_vector)):
    promezhut = eco_vector[k]+infrastructure_vector[k]+cash_vector[k] + realty_vector[k]
    itog_vector.append(promezhut)

print("Средневзвешенное значение:")
print("Москва:",itog_vector[0],"\nСанкт-Петербург:",itog_vector[1],"\nКазань:",itog_vector[2])
