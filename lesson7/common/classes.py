# -*- coding: utf-8 -*-

import socket
import sys
import json
import time
import logging
import select
import lesson7.logs.config_server_log
import lesson7.logs.config_client_log
from .variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE, MESSAGE_TEXT, MESSAGE, SENDER
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
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта {listen_port}'
                                   f'{listen_port}. Допустимы адреса с 1024 до 65535.')
            sys.exit(1)
        self.listen_address = listen_address
        self.listen_port = listen_port

    @log
    def process_client_message(message, messages_list, client):
        """
        Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
        проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
        :param message:
        :param messages_list:
        :param client:
        :return:
        """
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем, если успех
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            send_message(client, {RESPONSE: 200})
            return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and \
                TIME in message and MESSAGE_TEXT in message:
            messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
            return
        # Иначе отдаём Bad request
        else:
            send_message(client, {
                RESPONSE: 400,
                ERROR: 'Bad Request'
            })
            return

    @log
    def start(self):

        SERVER_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.listen_port}, '
            f'адрес с которого принимаются подключения: {self.listen_address}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(0.5)

        # список клиентов , очередь сообщений
        clients = []
        messages = []

        # Слушаем порт
        transport.listen(MAX_CONNECTIONS)
        # Основной цикл программы сервера
        while True:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = transport.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если там есть сообщения,
            # кладём в словарь, если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        ChatServer.process_client_message(get_message(client_with_message),
                                               messages, client_with_message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                    f'отключился от сервера.')
                        clients.remove(client_with_message)

            # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
            if messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: messages[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: messages[0][1]
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        send_message(waiting_client, message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                        waiting_client.close()
                        clients.remove(waiting_client)

    @log
    def stop(self):
        self.running = False


class ChatClient:
    client_user = USER
    server_address = DEFAULT_IP_ADDRESS
    server_port = DEFAULT_PORT
    mode = ""

    @log
    def __init__(self, username, server_address, server_port, mode):
        if not 1023 < server_port < 65536:
            CLIENT_LOGGER.critical(
                f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
            sys.exit(1)

        self.client_user = username
        self.server_address = server_address
        self.server_port = server_port
        self.client_mode = mode

    @log
    def message_from_server(self, message):
        """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
        if ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and MESSAGE_TEXT in message:
            print(f'Получено сообщение от пользователя '
                  f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                        f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        else:
            CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

    @log
    def create_message(sock, account_name='Guest'):
        """Функция запрашивает текст сообщения и возвращает его.
        Так же завершает работу при вводе подобной комманды
        """
        message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
        if message == '!!!':
            sock.close()
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            print('Спасибо за использование нашего сервиса!')
            sys.exit(0)
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: account_name,
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        return message_dict

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
    def process_response_ans(message):
        """
        Функция разбирает ответ сервера на сообщение о присутствии,
        возращает 200 если все ОК или генерирует исключение при ошибке
        """
        CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            elif message[RESPONSE] == 400:
                raise ServerError(f'400 : {message[ERROR]}')
        raise ReqFieldMissingError(RESPONSE)

    @log
    def messaging(self):
        CLIENT_LOGGER.info(
            f'Запущен клиент с парамертами: адрес сервера: {self.server_address}, '
            f'порт: {self.server_port}, режим работы: {self.client_mode}')

        # Инициализация сокета и сообщение серверу о нашем появлении
        try:
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.connect((self.server_address, self.server_port))
            send_message(transport, self.create_presence())
            answer = ChatClient.process_response_ans(get_message(transport))
            CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
            print(f'Установлено соединение с сервером.')
        except json.JSONDecodeError:
            CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
            sys.exit(1)
        except ServerError as error:
            CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
            sys.exit(1)
        except ReqFieldMissingError as missing_error:
            CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
            sys.exit(1)
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(
                f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}, '
                f'конечный компьютер отверг запрос на подключение.')
            sys.exit(1)
        else:
            # Если соединение с сервером установлено корректно,
            # начинаем обмен с ним, согласно требуемому режиму.
            # основной цикл прогрммы:
            if self.client_mode == 'send':
                print('Режим работы - отправка сообщений.')
            else:
                print('Режим работы - приём сообщений.')
            while True:
                # режим работы - отправка сообщений
                if self.client_mode == 'send':
                    try:
                        send_message(transport, ChatClient.create_message(transport))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        CLIENT_LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно.')
                        sys.exit(1)

                # Режим работы приём:
                if self.client_mode == 'listen':
                    try:
                        self.message_from_server(get_message(transport))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        CLIENT_LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно.')
                        sys.exit(1)


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


class ServerError(Exception):
    """Исключение - ошибка сервера"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
