import sys
from common.classes import ChatServer
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT

try:
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        listen_port = DEFAULT_PORT
    if listen_port < 1024 or listen_port > 65535:
        raise ValueError
except IndexError:
    print('После параметра -\'p\' необходимо указать номер порта.')
    sys.exit(1)
except ValueError:
    print(
        'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
    sys.exit(1)

try:
    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
    else:
        listen_address = DEFAULT_IP_ADDRESS
except IndexError:
    print(
        'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    sys.exit(1)


serv1 = ChatServer(listen_address, listen_port)

serv1.start()

serv1.stop()

print(serv1.listen_port)
