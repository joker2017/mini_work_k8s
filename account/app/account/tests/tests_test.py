
#from unittest.mock import patch
#from account.models import Account
#from account.views import AccountCreate, AccountList


import unittest
from unittest.mock import patch
#from myapp.models import Account  # Импорт модели Account из вашего приложения
#from account.app.app.services import create_account_number  # Предполагается, что функция определена в myapp/functions.py
from app.account.services import create_account_number
class CreateAccountNumberTest(unittest.TestCase):
    @patch('Account.objects.filter')
    def test_create_account_number_unique(self, mock_filter):
        # Настройка мока, чтобы возвращать пустой QuerySet, имитируя отсутствие совпадений в базе данных
        mock_filter.return_value.exists.return_value = False

        account_number = create_account_number()

        # Проверяем, что функция возвращает строку длиной 20 символов
        self.assertEqual(len(account_number), 20)
        # Проверяем, что функция generate_id вызывалась хотя бы один раз
        mock_filter.assert_called()

    @patch('Account.objects.filter')
    def test_create_account_number_retry_on_duplicate(self, mock_filter):
        # Настройка мока, чтобы сначала возвращать True, имитируя существующий номер счета,
        # а затем False, имитируя успешное создание уникального номера счета
        mock_filter.side_effect = [True, False]

        account_number = create_account_number()

        # Проверяем, что функция возвращает строку длиной 20 символов
        self.assertEqual(len(account_number), 20)
        # Проверяем, что функция generate_id была вызвана дважды: один раз для существующего номера счета и один раз для уникального
        self.assertEqual(mock_filter.call_count, 2)

if __name__ == '__main__':
    unittest.main()
