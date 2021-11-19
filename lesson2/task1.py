# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
# из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие
# и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения
# параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
# в соответствующий список. Должно получиться четыре списка —
# например, os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него
# названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
# через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().

import csv
import re

def get_data():
    files = ["info_1.txt", "info_2.txt", "info_3.txt"]
    os_prod_list = []
    os_code_list = []
    os_type_list = []
    os_name_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    for file in files:
        with open(file, 'r', encoding='cp1251') as f_n:
            for line in f_n:
                match_os_prod = re.search(r'(Изготовитель системы):\s+(.+)', line)
                if match_os_prod:
                    os_prod_list.append(match_os_prod.group(2))

                match_os_name = re.search(r'(Название ОС):\s+(.+)', line)
                if match_os_name:
                    os_name_list.append(match_os_name.group(2))

                match_os_code = re.search(r'(Код продукта):\s+(.+)', line)
                if match_os_code:
                    os_code_list.append(match_os_code.group(2))

                match_os_type = re.search(r'(Тип системы):\s+(.+)', line)
                if match_os_type:
                    os_type_list.append(match_os_type.group(2))

    for i in range(len(files)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data

def write_to_csv(file):
    data = get_data()
    with open(file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for line in data:
            writer.writerow(line)

    print(f'Файл {file} сформирован')


write_to_csv('report.csv')
