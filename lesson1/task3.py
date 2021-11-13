#3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
def check_convert_to_bytes(word_list):
    for word in word_list:
        convert_aviable = 1
        for i in range(len(word)):
            if ord(word[i]) > 127:
                convert_aviable = 0
                break
        if convert_aviable == 0:
            print(f'Слово {word} невозможно записать в байтовом типе')
        else:
            print(f'Слово {word} можно записать в байтовом типе')




words_list_str = ['attribute', 'класс', 'функция', "type"]

check_convert_to_bytes(words_list_str)