# test_services.py
import unittest
from unittest.mock import patch
from ..services import create_account_number
import pytest
from unittest.mock import patch

@patch('account.app.account.models.Account.objects.filter')
def test_create_account_number(mock_filter):
    mock_filter.return_value.exists.return_value = False

    account_number = create_account_number()

    assert len(account_number) == 20
    assert account_number.isdigit()
    mock_filter.assert_called()  # Или используйте assert_called_once_with(), если вы хотите проверить вызов с конкретными аргументами




import pytest
from unittest.mock import patch, MagicMock
from account.app.account.views import AccountCreate
from account.app.account.models import Account
from account.app.account.serializers import AccountSerializerRegistr
from account.app.account.services import create_account_number
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import status

# Фикстура для Request
@pytest.fixture
def fake_request():
    factory = APIRequestFactory()
    request = factory.post("/fake-url", {}, format='json')
    return Request(request)

@pytest.fixture
def account_data():
    return {
        "balance": "100.00",
        "id": "12345678901234567890",
        "usernameid": "test_user_id",  # предполагается, что это ForeignKey, укажите корректный ID
    }

@patch("account.app.account.views.AccountSerializerRegistr")
@patch("account.app.account.models.Account.objects.create")
@patch("account.app.account.services.create_account_number")
def test_account_create(mock_create_account_number, mock_account_create, mock_serializer_class, fake_request, account_data):
    # Настройка моков
    mock_create_account_number.return_value = '12345678901234567890'
    account_instance = Account(**account_data)
    mock_account_create.return_value = account_instance

    serializer_instance = MagicMock()
    mock_serializer_class.return_value = serializer_instance
    serializer_instance.is_valid.return_value = True
    serializer_instance.save.return_value = account_instance
    serializer_instance.data = account_data

    # Инициализация ViewSet и вызов метода create
    view = AccountCreate()
    view.request = fake_request
    view.format_kwarg = None

    response = view.create(fake_request)

    # Проверки
    mock_create_account_number.assert_called_once()
    mock_account_create.assert_called_once_with(**account_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == account_data
