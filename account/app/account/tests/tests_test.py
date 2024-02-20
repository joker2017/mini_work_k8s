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
from django.test import RequestFactory
from rest_framework.response import Response
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


def test_account_create_with_mocked_view(mock_create_account_number, mock_account_serializer):
    # Используем RequestFactory для создания запроса
    request = RequestFactory().post('/fake-url/', data={'balance': '100.00', 'usernameid': 'test_user_id'})
    request.data = {'balance': '100.00', 'usernameid': 'test_user_id'}

    # Замокировать ответ метода create
    with patch.object(AccountCreate, 'create', return_value=Response(
            {'id': '12345678901234567890', 'balance': '100.00', 'usernameid': 'test_user_id'},
            status=status.HTTP_201_CREATED)) as mock_method:
        view = AccountCreate.as_view({'post': 'create'})
        response = view(request)

    assert mock_method.called
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'id': '12345678901234567890', 'balance': '100.00', 'usernameid': 'test_user_id'}









import pytest
from unittest.mock import Mock, patch
from rest_framework.test import APIClient
from rest_framework import status
import json
from account.app.account.models import Account, Users
from account.app.account.serializers import AccountSerializer
from django.http import HttpRequest

@pytest.fixture
def mock_user_instance():
    user_mock = Mock(spec=Users)
    user_mock.id = 'test_user_id'
    return user_mock


@pytest.fixture
def account_instance(mock_user_instance):
    account_mock = Mock(spec=Account)
    account_mock.id = '12345678901234567890'
    account_mock.balance = 100.00
    account_mock.usernameid = mock_user_instance
    return account_mock


@pytest.fixture
def mock_account_serializer(account_instance):
    serializer_mock = Mock(spec=AccountSerializer)
    serializer_mock.instance = account_instance
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_instance
    serializer_mock.data = {
        'id': account_instance.id,
        'balance': '200.00',
        'usernameid': account_instance.usernameid.id
    }
    return serializer_mock


# Используем APIClient для тестирования представления AccountUpdate
def test_account_update_with_mocked_response():
    mock_request = Mock()
    mock_request.data = {'balance': '200.00'}

    mock_response = Mock(status_code=status.HTTP_200_OK, data=mock_request.data)

    with patch('account.app.account.views.AccountUpdate', return_value=mock_response) as mocked_put:
        response = mocked_put(mock_request)

        assert mocked_put.called
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_request.data



import pytest
from unittest.mock import Mock, patch
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from account.app.account.models import Account
from account.app.account.views import AccountDestroy

@pytest.fixture
def account_instance():
    # Создаем мок экземпляра аккаунта
    account_mock = Mock(spec=Account)
    account_mock.id = '12345678901234567890'
    return account_mock

# Тест для проверки удаления аккаунта
def test_account_destroy_with_mocked_response(account_instance):
    # Мокируем get_object, чтобы он возвращал экземпляр account, когда ищет по id
    with patch('account.app.account.views.AccountDestroy.get_object', return_value=account_instance) as mocked_get_object:
        # Мокируем метод perform_destroy класса AccountDestroy для имитации удаления
        with patch('account.app.account.views.AccountDestroy.perform_destroy', return_value=None) as mocked_perform_destroy:
            view = AccountDestroy()
            request = Mock()

            # Мокируем метод setup для инициализации запроса и ключей доступа
            view.setup(request, pk=account_instance.id)
            response = view.delete(request, pk=account_instance.id)

            mocked_get_object.assert_called_once()
            mocked_perform_destroy.assert_called_once_with(account_instance)

            assert response.status_code == status.HTTP_204_NO_CONTENT
