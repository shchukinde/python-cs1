#4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
# в байтовое и выполнить обратное преобразование (используя методы encode и decode).
def print_list_objects_types(word_list):
    for word in word_list:
        print(f'Слово "{word}" имеет тип {type(word)}')

def encode_list(word_list):
    b_word_list = []
    for word in word_list:
        b_word = word.encode('utf-8')
        b_word_list.append(b_word)
    return b_word_list

def decode_list(word_list):
    s_word_list = []
    for word in word_list:
        s_word = word.decode('utf-8')
        s_word_list.append(s_word)
    return s_word_list

words_list_str = ['разработка', 'администрирование', 'protocol', 'standard']

print('---исходный список слов и типы его объектов---')
print_list_objects_types(words_list_str)

print('---кодируем список и выводим на печать содержимое нового списка и типов объектов нём---')
bytes_word_list = encode_list(words_list_str)
print_list_objects_types(bytes_word_list)

print('---декодируем полученный список выше и выводим на печать содержимое нового списка и типов объектов нём---')
str_word_list = decode_list(bytes_word_list)
print_list_objects_types(str_word_list)
