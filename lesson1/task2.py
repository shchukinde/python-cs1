#2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
import ast

def convert_to_bytes(word_list):
    for word in word_list:
        byte_word = ast.literal_eval(f"b'{word}'")
        print(f'Слово {word} преобразованное в байты: '
              f'содержимое {byte_word}, '
              f'тип {type(byte_word)}, '
              f'длина {len(byte_word)}')

words_list_str = ['class', 'function', 'method']

convert_to_bytes(words_list_str)