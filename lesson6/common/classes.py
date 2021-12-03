import socket
import sys
import json
import time
import logging
import lesson5.logs.config_server_log
import lesson5.logs.config_client_log
from .variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE
from .utils import get_message, send_message
from .decos import log

# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


class ChatServer:
    listen_address = DEFAULT_IP_ADDRESS
    listen_port = DEFAULT_PORT
    running = False

    @log
    def __init__(self, listen_address, listen_port):
        if not 1023 < listen_port < 65536:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                   f'{listen_port}. Допустимы адреса с 1024 до 65535.')
            sys.exit(1)

        self.listen_address = listen_address
        self.listen_port = listen_port

    @log
    def process_client_message(self, message):
        '''
        Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клинта, проверяет корректность,
        возвращает словарь-ответ для клиента

        :param message:
        :return:
        '''
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Stop':
            self.running = False
            SERVER_LOGGER.critical(f'Получено сообщение от пользователя Stop. Сервер прекращает свою работу.')
            return {RESPONSE: 201}

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}

        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    @log
    def start(self):

        self.running = True

        # Готовим сокет

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))

        # Слушаем порт

        transport.listen(MAX_CONNECTIONS)

        SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {self.listen_port}, '
                           f'адрес с которого принимаются подключения: {self.listen_address}. '
                           f'Если адрес не указан, принимаются соединения с любых адресов.')

        while self.running:
            client, client_address = transport.accept()
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')

            try:
                message_from_client = get_message(client)
                SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
                response = ChatServer.process_client_message(self, message_from_client)
                SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
                send_message(client, response)
                SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
                client.close()
            except json.JSONDecodeError:
                SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от '
                                    f'клиента {client_address}. Соединение закрывается.')
                client.close()
            except IncorrectDataRecivedError:
                SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                    f'Соединение закрывается.')
                client.close()

    @log
    def stop(self):
        self.running = False


class ChatClient:
    client_user = USER
    server_address = DEFAULT_IP_ADDRESS
    server_port = DEFAULT_PORT

    @log
    def __init__(self, username, server_address, server_port):
        if not 1023 < server_port < 65536:
            CLIENT_LOGGER.critical(
                f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
            sys.exit(1)

        self.client_user = username
        self.server_address = server_address
        self.server_port = server_port

    @log
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
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.client_user}')
        return out

    @log
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

    @log
    def messaging(self):
        # Инициализация сокета и обмен
        try:
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                               f'адрес сервера: {self.server_address} , порт: {self.server_port}')
            transport.connect((self.server_address, self.server_port))
            message_to_server = self.create_presence()
            send_message(transport, message_to_server)
            answer = ChatClient.process_ans(get_message(transport))
            CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
            print(answer)

        except json.JSONDecodeError:
            CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')

        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        except ReqFieldMissingError as missing_error:
            CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                                f'{missing_error.missing_field}')


class IncorrectDataRecivedError(Exception):
    """
    Исключение  - некорректные данные получены от сокета
    """
    def __str__(self):
        return 'Принято некорректное сообщение от удалённого компьютера.'


class NonDictInputError(Exception):
    """
    Исключение - аргумент функции не словарь
    """
    def __str__(self):
        return 'Аргумент функции должен быть словарём.'


class ReqFieldMissingError(Exception):
    """
    Ошибка - отсутствует обязательное поле в принятом словаре
    """
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'
