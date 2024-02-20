# test_services.py
import unittest
from unittest.mock import patch
from app.account.services import create_account_number


class TestCreateAccountNumber(unittest.TestCase):
    @patch('account.app.account.models.Account.objects.filter')
    def test_create_account_number(self, mock_filter):
        # Настройка мока
        mock_filter.return_value.exists.return_value = False

        # Вызов функции
        account_number = create_account_number()

        # Проверки
        self.assertEqual(len(account_number), 20)
        self.assertTrue(account_number.isdigit())

        # Убедитесь, что мок был вызван
        mock_filter.assert_called()

if __name__ == '__main__':
    unittest.main()
