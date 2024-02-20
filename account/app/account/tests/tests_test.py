import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import RequestFactory, APIClient
from django.test import RequestFactory


from account.app.account.models import Account, Users
from account.app.account.views import AccountCreate, AccountUpdate, AccountDestroy
from account.app.account.serializers import AccountSerializerRegistr, AccountSerializer
from account.app.account.services import create_account_number

# Общие фикстуры для мокирования экземпляров пользователя и аккаунта
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

# Фикстура для мокирования сериализаторов
@pytest.fixture
def mock_account_serializer(account_instance, request):
    serializer_class = AccountSerializer if request.param == 'AccountSerializer' else AccountSerializerRegistr
    serializer_mock = Mock(spec=serializer_class)
    serializer_mock.instance = account_instance
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_instance
    serializer_mock.data = {
        'id': account_instance.id,
        'balance': account_instance.balance,
        'usernameid': account_instance.usernameid.id
    }
    return serializer_mock

# Тест для проверки функции создания номера счета
@patch('account.app.account.models.Account.objects.filter')
def test_create_account_number(mock_filter):
    mock_filter.return_value.exists.return_value = False
    assert len(create_account_number()) == 20
    assert create_account_number().isdigit()
    mock_filter.assert_called()

# Тесты для проверки создания и обновления аккаунта
@pytest.mark.parametrize('mock_account_serializer', ['AccountSerializerRegistr'], indirect=True)
def test_account_create_with_mocked_view(mock_create_account_number, mock_account_serializer):
    request = RequestFactory().post('/fake-url/', data={'balance': '100.00', 'usernameid': 'test_user_id'})
    request.data = {'balance': '100.00', 'usernameid': 'test_user_id'}
    with patch.object(AccountCreate, 'create', return_value=Response(
            mock_account_serializer.data, status=status.HTTP_201_CREATED)) as mock_method:
        response = AccountCreate.as_view({'post': 'create'})(request)
        assert mock_method.called
        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.parametrize('mock_account_serializer', ['AccountSerializer'], indirect=True)
def test_account_update_with_mocked_response(mock_account_serializer, account_instance):
    client = APIClient()
    updated_data = {'balance': '200.00'}
    with patch('account.app.account.views.AccountUpdate.get_object', return_value=account_instance), \
         patch('account.app.account.views.AccountUpdate.perform_update', return_value=None):
        response = client.put(f'/account/{account_instance.id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK

# Тест для проверки удаления аккаунта
def test_account_destroy_with_mocked_response(account_instance):
    with patch('account.app.account.views.AccountDestroy.get_object', return_value=account_instance), \
         patch('account.app.account.views.AccountDestroy.perform_destroy', return_value=None):
        view = AccountDestroy()
        request = Mock()
        view.setup(request, pk=account_instance.id)
        response = view.delete(request, pk=account_instance.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
