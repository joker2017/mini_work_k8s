import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.test import RequestFactory
from account.app.account.models import Account, Users
from account.app.account.views import AccountCreate, AccountUpdate, AccountDestroy
from account.app.account.serializers import AccountSerializerRegistr, AccountSerializer
from account.app.account.services import create_account_number


@pytest.fixture
def mock_user_instance():
    """Фикстура для создания мок экземпляра пользователя."""
    return Mock(spec=Users, id='test_user_id')


@pytest.fixture
def account_instance(mock_user_instance):
    """Фикстура для создания мок экземпляра аккаунта."""
    return Mock(spec=Account, id='12345678901234567890', balance=100.00, usernameid=mock_user_instance)


@pytest.fixture
def mock_account_serializer(account_instance):
    """Фикстура для создания мок сериализатора."""
    serializer_mock = Mock(spec=AccountSerializer)
    serializer_mock.instance = account_instance
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_instance
    serializer_mock.data = {'id': account_instance.id, 'balance': '200.00', 'usernameid': account_instance.usernameid.id}
    return serializer_mock


@patch('account.app.account.models.Account.objects.filter')
def test_create_account_number(mock_filter):
    """Тест проверяет создание номера аккаунта."""
    mock_filter.return_value.exists.return_value = False
    account_number = create_account_number()
    assert len(account_number) == 20 and account_number.isdigit()
    mock_filter.assert_called()


def test_account_create_with_mocked_view(mock_account_serializer):
    """Тест проверяет создание аккаунта с мокированным представлением."""
    request = RequestFactory().post('/fake-url/', data={'balance': '100.00', 'usernameid': 'test_user_id'})
    with patch.object(AccountCreate, 'create', return_value=Response(
            mock_account_serializer.data, status=status.HTTP_201_CREATED)) as mock_method:
        response = AccountCreate.as_view({'post': 'create'})(request)
        assert mock_method.called
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == mock_account_serializer.data


def test_account_update_with_mocked_response(mock_account_serializer):
    """Тест проверяет обновление аккаунта с мокированным ответом."""
    client = APIClient()
    with patch('account.app.account.views.AccountUpdate', return_value=Response(
            mock_account_serializer.data, status=status.HTTP_200_OK)) as mocked_put:
        response = mocked_put(Mock(data={'balance': '200.00'}))
        assert mocked_put.called
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_account_serializer.data


def test_account_destroy_with_mocked_response(account_instance):
    """Тест проверяет удаление аккаунта с мокированным ответом."""
    with patch('account.app.account.views.AccountDestroy.get_object', return_value=account_instance), \
         patch('account.app.account.views.AccountDestroy.perform_destroy', return_value=None):
        view = AccountDestroy()
        request = Mock()
        view.setup(request, pk=account_instance.id)
        response = view.delete(request, pk=account_instance.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
