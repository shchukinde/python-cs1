import socket
import sys
import json
import time
from .variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONDEFAULT_IP_ADDRESSSE
from .utils import get_message, send_message


class ChatServer:
    listen_address = DEFAULT_IP_ADDRESS
    listen_port = DEFAULT_PORT
    running = False

    def __init__(self, addr, port):
        try:
            if port < 1024 or port > 65535:
                raise ValueError
        except ValueError:
            print(
                'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        self.listen_address = addr
        self.listen_port = port

    def process_client_message(self, message):
        '''
        Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клинта, проверяет корректность,
        возвращает словарь-ответ для клиента

        :param message:
        :return:
        '''
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Stop':
            self.running = False
            return {RESPONSE: 201}

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}

        return {
            RESPONDEFAULT_IP_ADDRESSSE: 400,
            ERROR: 'Bad Request'
        }

    def start(self):

        self.running = True

        # Готовим сокет

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))

        # Слушаем порт

        transport.listen(MAX_CONNECTIONS)

        while self.running:
            client, client_address = transport.accept()
            try:
                message_from_cient = get_message(client)
                print(message_from_cient)
                response = ChatServer.process_client_message(self,message_from_cient)
                send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Принято некорретное сообщение от клиента.')
                client.close()

    def stop(self):
        self.running = False


class ChatClient:
    client_user = USER
    server_address = DEFAULT_IP_ADDRESS
    server_port = DEFAULT_PORT

    def __init__(self, username, server_address, server_port):
        try:
            if server_port < 1024 or server_port > 65535:
                raise ValueError
        except ValueError:
            print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        self.client_user = username
        self.server_address = server_address
        self.server_port = server_port

    def create_presence(self):
        '''
        Функция генерирует запрос о присутствии клиента
        :param account_name:
        :return:
        '''

        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_user
            }
        }
        return out

    def process_ans(message):
        '''
        Функция разбирает ответ сервера
        :param message:
        :return:
        '''
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ValueError

    def messaging(self):
        # Инициализация сокета и обмен

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((self.server_address, self.server_port))
        message_to_server = self.create_presence()
        send_message(transport, message_to_server)
        try:
            answer = ChatClient.process_ans(get_message(transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print('Не удалось декодировать сообщение сервера.')
