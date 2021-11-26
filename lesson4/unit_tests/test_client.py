"""Unit-тесты клиента"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from lesson4.common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from lesson4.common.classes import ChatClient


class TestClass(unittest.TestCase):
    '''
    Класс с тестами
    '''

    def test_def_presense(self):
        """Тест коректного запроса"""
        cl1 = ChatClient('Guest', '127.0.0.1', 5000)
        test = cl1.create_presence()
        test[TIME] = 1.1  # время необходимо приравнять принудительно
                          # иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_def_presense_negative(self):
        """Тест коректного запроса"""
        cl1 = ChatClient('Guest', '127.0.0.1', 5000)
        test = cl1.create_presence()
        test[TIME] = 1.1  # время необходимо приравнять принудительно
                          # иначе тест никогда не будет пройден
        self.assertNotEqual(test, {ACTION: "NOT_PRESENCE", TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(ChatClient.process_ans({RESPONSE: 200}), '200 : OK')

    def test_200_ans_negative(self):
        """Тест корректтного разбора ответа 200"""
        self.assertNotEqual(ChatClient.process_ans({RESPONSE: 200}), '300 : OK')

    def test_400_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(ChatClient.process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, ChatClient.process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
