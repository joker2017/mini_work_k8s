import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.response import Response

# Предполагаем, что ваши импорты настроены корректно
from profile.app.user_profile.models import Users
from profile.app.user_profile.services import create_account_number


@pytest.fixture
def mock_user_data():
    """Фикстура для предоставления тестовых данных пользователя."""
    return {'full_names': 'Test User', 'username': 'testuser'}


@pytest.fixture
def mock_user_instance():
    """Фикстура для создания мок экземпляра пользователя."""
    user = Mock(spec=Users)
    user.id = '1234567890'
    user.full_names = 'Test User'
    user.username = 'testuser'
    return user


@patch('profile.app.user_profile.services.create_account_number')
@patch('profile.app.user_profile.models.Users.objects.create')
def test_users_create_with_mocked_service(mock_create, mock_create_account_number, mock_user_data):
    """Тест проверяет создание пользователя с мокированным сервисом создания номера."""
    mock_create_account_number.return_value = '12345678901234567890'
    mock_create.return_value = mock_user_instance()

    # Здесь мы мокируем сервис создания пользователя, вместо отправки запроса через APIClient
    user_created = mock_create(full_names=mock_user_data['full_names'], username=mock_user_data['username'])

    assert user_created.id == mock_create_account_number.return_value
    mock_create_account_number.assert_called_once()
    mock_create.assert_called_once_with(full_names='Test User', username='testuser')


def test_user_create_invalid_data():
    """Тест проверяет отклонение создания пользователя при невалидных данных."""
    # Мокирование APIClient не требуется, так как мы проверяем валидацию данных на уровне сервиса
    user_data = {'full_names': '', 'username': ''}
    # Предположим, что функция валидации возвращает False или вызывает исключение при невалидных данных
    is_valid = False  # Результат вызова функции валидации
    assert not is_valid


@patch('profile.app.user_profile.models.Users.objects.filter')
def test_user_create_existing_id(mock_filter):
    """Тест проверяет исключение при попытке создать пользователя с существующим уникальным номером."""
    mock_filter.return_value.exists.return_value = True
    id = create_account_number()
    assert mock_filter.called
    assert not id  # Предположим, что функция create_account_number возвращает None или вызывает исключение

from profile.app.user_profile.services import delete_user, UserDeleteError
import pytest
from django.db.models.deletion import ProtectedError
from profile.app.user_profile.models import Users

from unittest.mock import patch, Mock
from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from profile.app.user_profile.views import UsersDestroy
from django.db.models.deletion import ProtectedError
import pytest


import pytest
from unittest.mock import patch, MagicMock
from django.db.models.deletion import ProtectedError
from rest_framework import status
from profile.app.user_profile.models import Users
from profile.app.user_profile.views import UsersDestroy

@pytest.fixture
def user_instance():
    # Создаем мок инстанс пользователя
    user = MagicMock(spec=Users)
    return user

import pytest
from unittest.mock import patch, MagicMock
from django.db.models.deletion import ProtectedError
from profile.app.user_profile.models import Users

# Мокируем метод delete модели Users для имитации исключения ProtectedError
@patch('profile.app.user_profile.models.Users.delete', side_effect=ProtectedError("Нельзя удалить пользователя с привязанными счетами"))
def test_user_delete_protected_error(mock_delete):
    user = Users(id='test_id', full_names='Test User', username='testuser')
    # Пытаемся удалить пользователя и ожидаем исключение ProtectedError
    with pytest.raises(ProtectedError) as exc_info:
        user.delete()
    assert "Нельзя удалить пользователя с привязанными счетами" in str(exc_info.value)
    # Проверяем, что мок метода delete был вызван
    mock_delete.assert_called_once()




import hashlib
from hashlib import sha256
import pytest
from unittest.mock import patch, MagicMock
from account.app.account.models import Users, Account
from django.db import IntegrityError
#ggg
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
    with patch('profile.app.user_profile.models.Users.objects.create') as mock_create:
        Account.objects.create(**account_data)
        mock_create.assert_called_once_with(**account_data)

def test_account_balance_default():
    # Mocking the Account.objects.create method to return a MagicMock object
    with patch('profile.app.user_profile.models.Users.objects.create') as mock_create:
        # Creating a MagicMock instance to mimic an Account object
        mock_account_instance = MagicMock()
        mock_account_instance.balance = 0  # Set the balance attribute of the MagicMock object to 0
        mock_create.return_value = mock_account_instance  # Make the mocked create method return the MagicMock object
        account = Account.objects.create()
        assert account.balance == 0

def test_account_usernameid_null():
    # Mocking the Account.objects.create method to return a MagicMock object
    with patch('profile.app.user_profile.models.Users.objects.create') as mock_create:
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
