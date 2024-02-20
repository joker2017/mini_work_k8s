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
from account.app.account.models import Account, Users
from account.app.account.views import AccountCreate
from account.app.account.serializers import AccountSerializerRegistr


@pytest.fixture
def mock_user_instance():
    # Создаем мок экземпляра пользователя
    user_mock = Mock(spec=Users)
    user_mock.id = 'test_user_id'
    return user_mock


@pytest.fixture
def mock_create_account_number(mocker):
    # Мокируем функцию создания номера аккаунта
    return mocker.patch('account.app.account.services.create_account_number', return_value='12345678901234567890')


@pytest.fixture
def mock_account_serializer(mocker, mock_user_instance):
    # Мокируем сериализатор для возвращения заданных данных
    account_mock = Mock(spec=Account)
    account_mock.id = '12345678901234567890'
    account_mock.balance = 100.00
    account_mock.usernameid = mock_user_instance
    serializer_mock = Mock(spec=AccountSerializerRegistr)
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_mock
    serializer_mock.data = {
        'id': account_mock.id,
        'balance': '100.00',
        'usernameid': account_mock.usernameid.id
    }
    return serializer_mock


def test_account_create(mock_create_account_number, mock_account_serializer, rf):
    # Используем RequestFactory для создания запроса
    request = rf.post('/fake-url/', data={'balance': '100.00', 'usernameid': 'test_user_id'})
    view = AccountCreate.as_view({'post': 'create'})

    # Создание мок-объекта response
    mock_response = Mock()
    mock_response.status_code = status.HTTP_201_CREATED
    #mock_response.data = {'id': '12345678901234567890', 'balance': '100.00', 'usernameid': 'test_user_id'}

    # Замокировать вызов view(request) и вернуть mock_response
    with patch('account.app.account.services.create_account_number', return_value='12345678901234567890'):
        with patch('account.app.account.views.AccountCreate.get_serializer', return_value=mock_account_serializer):
            with patch('account.app.account.views.AccountCreate') as mock_view:
                mock_view.return_value = view
                mock_view.return_value.return_value = mock_response
                response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    mock_create_account_number.assert_called_once()
    mock_account_serializer.is_valid.assert_called_once_with(raise_exception=True)
    mock_account_serializer.save.assert_called_once()
    assert response.data == {'id': '12345678901234567890', 'balance': '100.00', 'usernameid': 'test_user_id'}
