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
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.urls import reverse
from account.app.account.views import AccountCreate
from account.app.account.models import Account, Users
from account.app.account.serializers import AccountSerializerRegistr


@pytest.fixture
def account_data():
    return {
        'balance': '100.00',
        'id': '12345678901234567890',
        'usernameid': MagicMock(spec=Users)  # Имитация экземпляра Users
    }


@pytest.fixture
def account_serializer_data():
    return {
        'balance': '100.00',
        'id': '12345678901234567890',
        'usernameid': 'test_user_id'
    }


@pytest.mark.django_db
@patch('account.app.account.serializers.AccountSerializerRegistr')
@patch('account.app.account.services.create_account_number')
@patch('account.app.account.models.Account.objects.create')
def test_account_create(mock_account_create, mock_create_account_number, mock_serializer_class, account_data,
                        account_serializer_data):
    mock_create_account_number.return_value = '12345678901234567890'
    mock_account_create.return_value = Account(**account_data)
    mock_serializer_class.return_value = MagicMock(data=account_serializer_data)
    mock_serializer_class.return_value.is_valid.return_value = True
    mock_serializer_class.return_value.save.return_value = mock_account_create.return_value
    mock_serializer_class.return_value.data = account_serializer_data

    factory = APIRequestFactory()
    view = AccountCreate.as_view({'post': 'create'})

    request = factory.post(reverse('account-create'), account_serializer_data, format='json')
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_account_create.assert_called_once_with(id='12345678901234567890', balance='100.00',
                                                usernameid=account_data['usernameid'])
    mock_serializer_class.assert_called_once_with(data=account_serializer_data)
