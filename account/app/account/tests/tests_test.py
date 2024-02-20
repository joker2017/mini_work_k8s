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
from unittest.mock import Mock, patch
from rest_framework import status

# Assuming these are the correct paths to your actual implementations
from account.app.account.views import AccountCreate
from account.app.account.models import Account
from account.app.account.serializers import AccountSerializerRegistr

@pytest.fixture
def mock_create_account_number(mocker):
    return mocker.patch('account.app.account.services.create_account_number', return_value='12345678901234567890')

@pytest.fixture
def mock_account_save(mocker):
    return mocker.patch.object(Account, 'save', autospec=True)

@pytest.fixture
def mock_serializer(mocker):
    # This mock setup assumes the serializer's save method is used and it returns an Account instance
    account_instance = Account(id='12345678901234567890', balance=100.00, usernameid='test_user_id')
    serializer_mock = Mock(spec=AccountSerializerRegistr)
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_instance
    serializer_mock.data = {
        'id': account_instance.id,
        'balance': str(account_instance.balance),
        'usernameid': account_instance.usernameid
    }
    return mocker.patch('account.app.account.views.AccountSerializerRegistr', return_value=serializer_mock)

def test_account_create(mock_create_account_number, mock_account_save, mock_serializer):
    view = AccountCreate()
    request = Mock()
    request.data = {
        'balance': '100.00',
        'usernameid': 'test_user_id'
    }
    # Setup request object as DRF does
    request._request = Mock()
    request.user = None

    # Patch the get_serializer method to use the mock serializer
    with patch.object(AccountCreate, 'get_serializer', return_value=mock_serializer):
        response = view.create(request)

    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_serializer.is_valid.assert_called_once_with(raise_exception=True)
    mock_serializer.save.assert_called_once()
    assert response.data['id'] == '12345678901234567890'
    assert response.data['balance'] == '100.00'
    assert response.data['usernameid'] == 'test_user_id'
