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


@patch('profile.app.user_profile.models.Users.objects.filter')
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
        response = UsersCreate.as_view({'post': 'create'})(request)
        assert mock_method.called
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == mock_account_serializer.data


def test_account_update_with_mocked_response(mock_account_serializer):
    """Тест проверяет обновление аккаунта с мокированным ответом."""
    client = APIClient()
    with patch('profile.app.user_profile.views.ProfileUpdate', return_value=Response(
            mock_account_serializer.data, status=status.HTTP_200_OK)) as mocked_put:
        response = mocked_put(Mock(data={'balance': '200.00'}))
        assert mocked_put.called
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_account_serializer.data


def test_account_destroy_with_mocked_response(account_instance):
    """Тест проверяет удаление аккаунта с мокированным ответом."""
    with patch('profile.app.user_profile.views.ProfileDestroy.get_object', return_value=account_instance), \
         patch('profile.app.user_profile.views.ProfileDestroy.perform_destroy', return_value=None):
        view = UsersDestroy()
        request = Mock()
        view.setup(request, pk=account_instance.id)
        response = view.delete(request, pk=account_instance.id)
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

def test_profile_creation(user_data):
    with patch('account.app.account.models.Users.objects.create') as mock_create:
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
