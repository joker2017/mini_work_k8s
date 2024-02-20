from django.test import TestCase
from unittest.mock import patch
from account.models import Account
from account.views import AccountCreate, AccountList
from django.http import HttpRequest
from django.test.utils import override_settings
import pytest

# Мок функции, которая будет использоваться для подмены вызовов к модели Account
def mock_account_save(self, *args, **kwargs):
    # Можете добавить логику для сохранения данных мока, если это необходимо
    pass


def mock_account_objects_all(self, *args, **kwargs):
    # Здесь возвращаем мокированный список аккаунтов, например:
    return [Account(name="Test Account")]

@pytest.fixture(scope='session')
def django_db_setup():
    """Переопределение фикстуры для предотвращения создания тестовой БД."""
    pass

class AccountTests(TestCase):
    @override_settings(DATABASES={"default": {"ENGINE": "django.db.backends.dummy"}})
    @patch('app.models.Account.save', mock_account_save)
    def test_create_account(self):
        # Здесь мы создаем тестовый запрос и вызываем нашу функцию создания аккаунта
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = "Test Account"

        response = create_account(request)
        self.assertEqual(response.status_code, 200)
        # Дополнительные проверки

    @patch('app.models.Account.objects.all', mock_account_objects_all)
    def test_list_accounts(self):
        # Здесь мы создаем тестовый запрос и вызываем нашу функцию списка аккаунтов
        request = HttpRequest()
        response = list_accounts(request)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе содержится информация о мокированных аккаунтах
        self.assertIn("Test Account", response.content.decode())
