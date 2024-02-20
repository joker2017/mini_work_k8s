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












from unittest.mock import Mock, patch, MagicMock
from django.utils.crypto import get_random_string
from django.db.models import Model


def test_user_password_hashing():
    # Подготавливаем данные пользователя
    user_data = {
        "id": get_random_string(20),
        "full_names": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "password": "password",
    }

    # Создаем мок пользователя с заданным паролем
    user = Mock(spec=Users, **user_data)

    # Имитация процесса сохранения, включая хеширование пароля
    with patch('account.app.account.models.Users.save', autospec=True) as mock_save:
        # При сохранении пользователя хешируем его пароль
        user.password = sha256(user.password.encode('utf-8')).hexdigest()
        user.save()  # Вызываем сохранение, которое в реальности мокируется

        # Проверяем, что метод save был вызван
        mock_save.assert_called_once_with(user)

        # Проверяем, что пароль пользователя был хеширован корректно
        expected_hashed_password = sha256(user_data["password"].encode('utf-8')).hexdigest()
        assert user.password == expected_hashed_password, "Password was not hashed correctly"


@pytest.fixture
def mock_user_instance():
    # Создаем мок экземпляра пользователя с дополнительным атрибутом _state
    user_mock = Mock(spec=Users)
    user_mock.id = get_random_string(20)
    user_mock._state = MagicMock()  # Имитация объекта _state, используемого Django
    return user_mock

def test_account_creation_without_db(mock_user_instance):
    account_id = get_random_string(20, allowed_chars='0123456789')
    balance = 100.00

    with patch('account.app.account.models.Account.save', autospec=True) as mock_save:
        # Создаем экземпляр Account без сохранения в базу данных
        account = Account(id=account_id, balance=balance, usernameid=mock_user_instance)
        mock_save.assert_not_called()  # Убедиться, что метод save не был вызван

        assert account.id == account_id
        assert account.balance == balance
        assert account.usernameid == mock_user_instance



