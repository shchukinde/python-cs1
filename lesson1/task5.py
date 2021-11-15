#5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
#и преобразовать результаты из байтовового в строковый тип на кириллице.
import subprocess
import chardet

def ping_decode(host):
    args = ['ping', host, '-c','4']
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        code = chardet.detect(line)
        print(f'Строка {line} из вывода пришла в кодировке', code['encoding'])
        line = line.decode(code['encoding'])
        line = line.encode('cp1251')
        code = chardet.detect(line)
        print(f'Перекодированная строка {line} имеет кодировку', code['encoding'])
        print('Итоговая строка:', line.decode(code['encoding']))

ping_decode('yandex.ru')
ping_decode('youtube.com')

# У меня везде писало что кодировка ascii, что до кодирования, что после.
# Скорее всего это связано с тем, что у меня вывод пинга пишется по английски и chardet, по всей видимости, считает,
# что это ascii, т.к. там все символы  действительно до 127. Ниже пример, в котором я разбирался, что кодировка меняется
#
# line=bytes('\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', 'cp1251')
# code = chardet.detect(line)
# print(code)
# line=line.decode(code['encoding'])
# print(line)
# line=line.encode('utf-8')
# code = chardet.detect(line)
# print(code)
# print(line.decode(code['encoding']))
