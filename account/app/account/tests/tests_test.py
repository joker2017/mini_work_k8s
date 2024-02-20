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











from rest_framework import status
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_create_account_number(mocker):
    return mocker.patch('account.app.account.services.create_account_number', return_value='12345678901234567890')

@pytest.fixture
def mock_account_save(mocker):
    return mocker.patch('account.app.account.models.Account.save', autospec=True)

@pytest.fixture
def mock_serializer_context(mocker):
    return mocker.patch('account.app.account.views.AccountCreate.get_serializer_context', return_value={'request': Mock(), 'view': Mock()})

@pytest.fixture
def mock_serializer_is_valid(mocker):
    serializer_mock = Mock()
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = None
    serializer_mock.data = {
        'id': '12345678901234567890',
        'balance': '100.00',
        'usernameid': 'test_user_id'
    }
    return mocker.patch('account.app.account.views.AccountSerializerRegistr.is_valid', return_value=serializer_mock)

@pytest.fixture
def mock_serializer_save(mocker):
    return mocker.patch('account.app.account.views.AccountSerializerRegistr.save')

def test_account_create(mock_create_account_number, mock_serializer_context, mock_serializer_is_valid, mock_serializer_save):
    from account.app.account.views import AccountCreate

    # Подготовка объекта view и запроса
    view = AccountCreate()
    request = Mock(data={
        'balance': '100.00',
        'usernameid': 'test_user_id'
    })
    request._request = Mock()  # Эмуляция HttpRequest объекта

    # Вызов метода create и проверка результатов
    response = view.create(request)
    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_serializer_is_valid.assert_called_once()
    mock_serializer_save.assert_called_once()
