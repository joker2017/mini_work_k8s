import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.test import RequestFactory
from account.app.account.models import Account, Users
from profile.app.user_profile.views import UsersCreate, UsersUpdate, UsersDestroy
from profile.app.user_profile.serializers import UsersSerializer
from profile.app.user_profile.services import create_account_number

@pytest.fixture
def mock_users_instance():
    """Фикстура для создания мок экземпляра пользователя."""
    return Mock(spec=Users, full_names='boris efimovich', username='boris', email='boris@ya.ru', password='123abc', id='12345678901234567890')

@pytest.fixture
def users_instance():
    """Фикстура для создания мок экземпляра пользователя."""
    return Mock(spec=Users, full_names='Ivan Petrov', username='ivan', email='ivan@ya.ru', password='1234567890', id='98765432109876543210')

@pytest.fixture
def mock_users_serializer(users_instance):
    """Фикстура для создания мок сериализатора."""
    serializer_mock = Mock(spec=UsersSerializer)
    serializer_mock.instance = users_instance
    serializer_mock.is_valid.return_value = True
    serializer_mock.save.return_value = users_instance
    serializer_mock.data = {
        'full_names': users_instance.full_names,
        'username': users_instance.username,
        'email': users_instance.email,
        'password': users_instance.password,
        'id': users_instance.id
    }
    return serializer_mock


@patch('profile.app.user_profile.models.Users.objects.filter')
def test_create_profile_number(mock_filter):
    """Тест проверяет создание номера аккаунта."""
    mock_filter.return_value.exists.return_value = False
    users_number = create_account_number()
    assert len(users_number) == 20 and users_number.isdigit()
    mock_filter.assert_called()


def test_profile_create_with_mocked_view(mock_users_serializer):
    """Тест проверяет создание аккаунта с мокированным представлением."""
    request = RequestFactory().post('/fake-url/', data={'full_names': 'ivan', 'username': 'test_user_id', 'email': 'ivan@ya.ru', 'password': '1234567890', 'id': '12345678901234567890'})
    with patch.object(UsersCreate, 'create', return_value=Response(
            mock_users_serializer.data, status=status.HTTP_201_CREATED)) as mock_method:
        response = UsersCreate.as_view({'post': 'create'})(request)
        assert mock_method.called
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == mock_users_serializer.data


def test_users_update_with_mocked_response(mock_users_serializer):
    """Тест проверяет обновление аккаунта с мокированным ответом."""
    client = APIClient()
    with patch('profile.app.user_profile.views.UsersUpdate', return_value=Response(
            mock_users_serializer.data, status=status.HTTP_200_OK)) as mocked_put:
        response = mocked_put(Mock(data={'balance': '200.00'}))
        assert mocked_put.called
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_users_serializer.data


def test_users_destroy_with_mocked_response(users_instance):
    """Тест проверяет удаление аккаунта с мокированным ответом."""
    with patch('profile.app.user_profile.views.UsersDestroy.get_object', return_value=users_instance), \
         patch('profile.app.user_profile.views.UsersDestroy.perform_destroy', return_value=None):
        view = UsersDestroy()
        request = Mock()
        view.setup(request, pk=users_instance.id)
        response = view.delete(request, pk=users_instance.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT





















import hashlib
from hashlib import sha256
import pytest
from unittest.mock import patch, MagicMock
from profile.app.user_profile.models import Users, Account
from django.db import IntegrityError

@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'full_names': 'Test User',
        'id': 'test_id',
        'password': 'password123',
        'username': 'test_user'
    }
@pytest.fixture
def account_data():
    return {
        'id': 'test_account_id',
        'balance': 100.00,
        'usernameid': None  # You can replace None with a Users instance if needed
    }
def test_user_creation(user_data):
    with patch('profile.app.user_profile.models.Users.objects.create') as mock_create:
        Users.objects.create(**user_data)
        mock_create.assert_called_once_with(**user_data)

def test_unique_username_constraint(user_data):
    with patch('profile.app.user_profile.models.Users.objects.create') as mock_create:
        mock_create.side_effect = [None, IntegrityError()]
        Users.objects.create(**user_data)  # Creating the first user
        with pytest.raises(IntegrityError):
            Users.objects.create(**user_data)  # Attempt to create a user with the same username

def test_account_creation(account_data):
    with patch('profile.app.user_profile.models.Account.objects.create') as mock_create:
        Account.objects.create(**account_data)
        mock_create.assert_called_once_with(**account_data)

def test_account_balance_default():
    # Mocking the Account.objects.create method to return a MagicMock object
    with patch('profile.app.user_profile.models.Account.objects.create') as mock_create:
        # Creating a MagicMock instance to mimic an Account object
        mock_account_instance = MagicMock()
        mock_account_instance.balance = 0  # Set the balance attribute of the MagicMock object to 0
        mock_create.return_value = mock_account_instance  # Make the mocked create method return the MagicMock object
        account = Account.objects.create()
        assert account.balance == 0

def test_account_usernameid_null():
    # Mocking the Account.objects.create method to return a MagicMock object
    with patch('profile.app.user_profile.models.Account.objects.create') as mock_create:
        # Creating a MagicMock instance to mimic an Account object
        mock_account_instance = MagicMock()
        mock_account_instance.usernameid = None  # Set the usernameid attribute of the MagicMock object to None
        mock_create.return_value = mock_account_instance  # Make the mocked create method return the MagicMock object
        account = Account.objects.create()
        assert account.usernameid is None


def test_user_password_hashing(user_data):
    with patch.object(Users, 'save', autospec=True) as mock_save:
        user = Users(**user_data)
        # Хешируем пароль перед сохранением
        user.password = sha256(user.password.encode('utf-8')).hexdigest()
        user.save()
        mock_save.assert_called_once()
        saved_password = user.password
        # Хешируем ожидаемый пароль
        expected_hashed_password = sha256(user_data['password'].encode('utf-8')).hexdigest()
        # Сравниваем хешированные пароли
        assert saved_password == expected_hashed_password
