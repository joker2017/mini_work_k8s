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
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def mock_create_account_number(mocker):
    return mocker.patch('account.services.create_account_number', return_value='12345678901234567890')

@pytest.fixture
def mock_account_save(mocker):
    return mocker.patch('account.models.Account.save', autospec=True)

@pytest.fixture
def client():
    return APIClient()

def test_account_create(client, mock_create_account_number, mock_account_save):
    account_data = {
        'balance': '100.00',
        'usernameid': 'test_user_id'
    }

    url = reverse('account-create')

    response = client.post(url, account_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_account_save.assert_called_once()

    assert response.data['id'] == '12345678901234567890'
    assert response.data['balance'] == '100.00'
    assert response.data['usernameid'] == 'test_user_id'

