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
from unittest.mock import Mock, patch, create_autospec
from rest_framework import status
from account.app.account.models import Account, Users
from account.app.account.views import AccountCreate
from account.app.account.serializers import AccountSerializerRegistr

@pytest.fixture
def user_instance():
    # Create a mock Users instance
    user_mock = create_autospec(Users, instance=True)
    user_mock.id = 'test_user_id'
    return user_mock

@pytest.fixture
def mock_create_account_number(mocker):
    return mocker.patch('account.app.account.services.create_account_number', return_value='12345678901234567890')

@pytest.fixture
def mock_account_save(mocker):
    return mocker.patch.object(Account, 'save', autospec=True)

@pytest.fixture
def mock_serializer(mocker, user_instance):
    # Mock the AccountSerializerRegistr to return a specific data structure
    # Ensure it returns a mock account instance with a mock Users instance as usernameid
    account_mock = Mock(spec=Account)
    account_mock.id = '12345678901234567890'
    account_mock.balance = 100.00
    account_mock.usernameid = user_instance
    serializer_mock = Mock(spec=AccountSerializerRegistr)
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_mock
    serializer_mock.data = {
        'id': account_mock.id,
        'balance': str(account_mock.balance),
        'usernameid': account_mock.usernameid.id
    }
    return mocker.patch('account.app.account.views.AccountCreate.get_serializer', return_value=serializer_mock)

def test_account_create(mock_create_account_number, mock_account_save, mock_serializer, user_instance):
    # Patch the AccountCreate view to use the mock serializer and bypass actual DB calls
    view = AccountCreate()
    request = Mock()
    request.data = {
        'balance': '100.00',
        'usernameid': user_instance.id
    }
    request._request = Mock()
    request.user = None

    response = view.create(request)

    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_serializer().is_valid.assert_called_once_with(raise_exception=True)
    mock_serializer().save.assert_called_once()
    assert response.data['id'] == '12345678901234567890'
    assert response.data['balance'] == '100.00'
    assert response.data['usernameid'] == user_instance.id
