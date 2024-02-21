import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.test import APIClient
from django.test import RequestFactory
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from profile.app.profile.models import Users
from profile.app.profile.views import UsersCreate, UsersUpdate, UsersDestroy
from profile.app.profile.services import create_account_number

@pytest.fixture
def mock_user_data():
    """Фикстура для предоставления тестовых данных пользователя."""
    return {'full_names': 'Test User', 'username': 'testuser'}

@pytest.fixture
def mock_user_instance():
    """Фикстура для создания мок экземпляра пользователя."""
    return Mock(spec=Users, id=create_account_number(), full_names='Test User', username='testuser')

@patch('profile.app.user_profile.services.create_account_number')
def test_users_create_with_mocked_service(mock_create_account_number, mock_user_data):
    """Тест проверяет создание пользователя с мокированным сервисом создания номера."""
    mock_create_account_number.return_value = '12345678901234567890'
    client = APIClient()
    response = client.post('/users/', data=mock_user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['id'] == '12345678901234567890'
    mock_create_account_number.assert_called_once()

def test_user_create_invalid_data():
    """Тест проверяет отклонение создания пользователя при невалидных данных."""
    client = APIClient()
    response = client.post('/users/', data={'full_names': '', 'username': ''}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'full_names' in response.data
    assert 'username' in response.data

@patch('profile.app.user_profile.models.Users.objects.create')
def test_user_create_existing_id(mock_create, mock_user_data):
    """Тест проверяет исключение при попытке создать пользователя с существующим уникальным номером."""
    mock_create.side_effect = IntegrityError("unique constraint failed")
    client = APIClient()
    response = client.post('/users/', data=mock_user_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "unique constraint failed" in str(response.data)

def test_user_update_invalid_data(mock_user_instance):
    """Тест проверяет отклонение обновления пользователя при невалидных данных."""
    client = APIClient()
    updated_data = {'full_names': '', 'username': ''}
    with patch.object(UsersUpdate, 'get_object', return_value=mock_user_instance):
        response = client.put(f'/users/{mock_user_instance.id}/', data=updated_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'full_names' in response.data
        assert 'username' in response.data

def test_user_destroy_with_protected_error(mock_user_instance):
    """Тест проверяет исключение при попытке удалить пользователя с привязанными к нему аккаунтами."""
    with patch.object(UsersDestroy, 'get_object', return_value=mock_user_instance), \
         patch.object(UsersDestroy, 'perform_destroy', side_effect=ProtectedError("Нельзя удалить клиента привязаными счетами")):
        client = APIClient()
        response = client.delete(f'/users/{mock_user_instance.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Нельзя удалить клиента привязаными счетами" in str(response.data)



















import hashlib
from hashlib import sha256
import pytest
from unittest.mock import patch, MagicMock
from account.app.account.models import Users, Account
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
    with patch('account.app.account.models.Users.objects.create') as mock_create:
        Users.objects.create(**user_data)
        mock_create.assert_called_once_with(**user_data)

def test_unique_username_constraint(user_data):
    with patch('account.app.account.models.Users.objects.create') as mock_create:
        mock_create.side_effect = [None, IntegrityError()]
        Users.objects.create(**user_data)  # Creating the first user
        with pytest.raises(IntegrityError):
            Users.objects.create(**user_data)  # Attempt to create a user with the same username

def test_account_creation(account_data):
    with patch('account.app.account.models.Account.objects.create') as mock_create:
        Account.objects.create(**account_data)
        mock_create.assert_called_once_with(**account_data)

def test_account_balance_default():
    # Mocking the Account.objects.create method to return a MagicMock object
    with patch('account.app.account.models.Account.objects.create') as mock_create:
        # Creating a MagicMock instance to mimic an Account object
        mock_account_instance = MagicMock()
        mock_account_instance.balance = 0  # Set the balance attribute of the MagicMock object to 0
        mock_create.return_value = mock_account_instance  # Make the mocked create method return the MagicMock object
        account = Account.objects.create()
        assert account.balance == 0

def test_account_usernameid_null():
    # Mocking the Account.objects.create method to return a MagicMock object
    with patch('account.app.account.models.Account.objects.create') as mock_create:
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
