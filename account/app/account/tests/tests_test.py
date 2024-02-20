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
from unittest.mock import patch, create_autospec
from account.app.account.models import Account
from account.app.account.services import create_account_number
from account.app.account.views import AccountCreate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from account.app.account.serializers import AccountSerializerRegistr

@pytest.fixture
def account_data():
    return {
        'id': '12345678901234567890',
        'balance': '100.00',
        'usernameid': 'test_user_id'
    }

@pytest.fixture
def account_instance(account_data):
    account = Account(**account_data)
    account.save = lambda: None  # Предотвращаем попытку сохранения в базу данных
    return account

@patch('account.app.account.serializers.AccountSerializerRegistr')
@patch('account.app.account.services.create_account_number')
@patch('account.app.account.models.Account.objects.create')
def test_account_create(mock_account_create, mock_create_account_number, mock_serializer_class, account_data, account_instance):
    mock_create_account_number.return_value = account_data['id']
    mock_account_create.return_value = account_instance
    mock_serializer = create_autospec(AccountSerializerRegistr)
    mock_serializer.is_valid.return_value = True
    mock_serializer.save.return_value = account_instance
    mock_serializer.instance = account_instance
    mock_serializer.data = account_data
    mock_serializer_class.return_value = mock_serializer

    view = AccountCreate.as_view({'post': 'create'})
    factory = APIRequestFactory()
    request = factory.post('/fake-url', account_data, format='json')
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_account_create.assert_called_once_with(id=account_data['id'], balance=account_data['balance'], usernameid=account_data['usernameid'])
    mock_serializer_class.assert_called_once_with(data=request.data)
    mock_serializer.is_valid.assert_called_once()
    mock_serializer.save.assert_called_once()
