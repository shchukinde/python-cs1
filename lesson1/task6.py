#6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
import locale
import chardet

str_list = ['сетевое программирование', 'сокет', 'декоратор']

#Проверим кодировку по-умолчанию. У меня UTF8.
def_coding = locale.getpreferredencoding()
print('Кодировка по умолчанию в системе:', def_coding)

#Пишем файл
with open('test_file.txt', 'w') as f_n:
    for el_str in str_list:
        f_n.write(f'{el_str}\n')

#Читаем файл, попутно перекодируя его в utf-8
print('Читаем файл в кодировке utf-8')
with open('test_file.txt', 'rb') as f_n:
    for line in f_n:
        code = chardet.detect(line)
        line = line.decode(code['encoding'])
        line = line.encode('utf-8')
        print(line.decode('utf-8'))
