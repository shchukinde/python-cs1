# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.
def print_types(word_list):
    for word in word_list:
        print(f'Слово {word} имеет тип {type(word)}')

words_list_str = ['разработка', 'сокет', 'декоратор']
words_list_utf = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                  '\u0441\u043e\u043a\u0435\u0442',
                  '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
print("---Печатаем строковый список слов---")
print_types(words_list_str)
print("---Печатаем список слов в юникоде---")
print_types(words_list_utf)
