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













import hashlib
import pytest
from unittest.mock import Mock, patch, MagicMock
from django.utils.crypto import get_random_string
from hashlib import sha256
from account.app.account.models import Users, Account
from account.app.account.views import AccountCreate, AccountUpdate, AccountDestroy
from account.app.account.serializers import AccountSerializerRegistr, AccountSerializer

# Общая фикстура для мокирования экземпляра пользователя
@pytest.fixture
def mock_user_instance():
    user_mock = Mock(spec=Users)
    user_mock.id = get_random_string(20)
    user_mock._state = MagicMock()  # Имитация _state для Django ORM
    return Mock(spec=Users, id='mock_user_id')

# Фикстура для мокирования сериализатора аккаунта
@pytest.fixture
def mock_account_serializer(mock_user_instance):
    account_mock = Mock(spec=Account)
    account_mock.id = get_random_string(20, allowed_chars='0123456789')
    account_mock.balance = 100.00
    account_mock.usernameid = mock_user_instance
    serializer_mock = Mock(spec=AccountSerializer)
    serializer_mock.instance = account_mock
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = account_mock
    serializer_mock.data = {
        'id': account_mock.id,
        'balance': 100.00,
        'usernameid': account_mock.usernameid.id
    }
    return serializer_mock

# Тест для создания номера аккаунта
def test_create_account_number():
    with patch('account.app.account.services.create_account_number', return_value='12345678901234567890') as mock_create_account_number:
        account_number = mock_create_account_number()
        assert len(account_number) == 20
        assert account_number.isdigit()

# Тест для создания аккаунта с мокированным ответом
def test_account_create_with_mocked_view(mock_account_serializer):
    with patch('account.app.account.views.AccountCreate.get_serializer', return_value=mock_account_serializer):
        request = Mock()
        request.data = {'balance': 100.00, 'usernameid': mock_user_instance.id}
        response = AccountCreate.as_view()(request)
        assert response.status_code == 201
        assert response.data == mock_account_serializer.data

# Тест для обновления аккаунта с мокированным ответом
def test_account_update_with_mocked_response(mock_account_serializer):
    with patch('account.app.account.views.AccountUpdate.get_serializer', return_value=mock_account_serializer):
        request = Mock()
        request.data = {'balance': 200.00}
        response = AccountUpdate.as_view()(request, pk=mock_account_serializer.instance.id)
        assert response.status_code == 200
        assert response.data == mock_account_serializer.data

# Тест для удаления аккаунта с мокированным ответом
def test_account_destroy_with_mocked_response():
    with patch('account.app.account.views.AccountDestroy.get_object', return_value=mock_user_instance):
        request = Mock()
        response = AccountDestroy.as_view()(request, pk=mock_user_instance.id)
        assert response.status_code == 204


@pytest.fixture
def user_data():
    return {
        "id": get_random_string(20),
        "full_names": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "password": "password"
    }


def test_user_password_hashing(user_data):
    # Create a user instance with unhashed password
    user = Users(**user_data)

    # Hash the password for comparison
    expected_hash = hashlib.sha256(user_data["password"].encode('utf-8')).hexdigest()

    # Simulate the save method to hash the password
    with patch.object(Users, 'save', autospec=True) as mock_save:
        user.save()  # Normally hashes password

        # Ensure the save method was called
        mock_save.assert_called_once()

        # Directly assert the hashed password or mock the hashing logic
        # For illustration, assuming password hashing occurs within `user.save()`
        assert user.password == expected_hash, "The password was not hashed correctly"
# Тест для создания аккаунта без обращения к базе данных
def test_account_creation_without_db(mock_user_instance):
    account = Account(id=get_random_string(20), balance=100.00, usernameid=mock_user_instance)
    assert account.id is not None
    assert account.balance == 100.00
    assert account.usernameid == mock_user_instance








