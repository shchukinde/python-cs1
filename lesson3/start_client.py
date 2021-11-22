import sys
from common.classes import ChatClient
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT

try:
    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    if server_port < 1024 or server_port > 65535:
        raise ValueError
except IndexError:
    server_address = DEFAULT_IP_ADDRESS
    server_port = DEFAULT_PORT
except ValueError:
    print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
    sys.exit(1)

client1 = ChatClient('Guest', server_address, server_port)

client1.messaging()

client2 = ChatClient('Stop', server_address, server_port)

client2.messaging()
