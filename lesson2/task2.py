# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров —
# товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

import json

def write_order_to_json(item, quantity, price, buyer, date):
    data={}
    with open("orders.json", encoding="utf-8") as json_file:
        data = json.loads(json_file.read())

    data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open("orders.json", 'w',encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4,  ensure_ascii=False)

    print("Данные о новом заказе записаны")

write_order_to_json("ручка", 7, 12, "Вася Пупкин", "19.11.2021")
write_order_to_json("карандаш", 22, 5, "Иван Таранов", "11.11.2021")
