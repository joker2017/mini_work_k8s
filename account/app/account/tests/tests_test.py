# import pytest
# from hashlib import sha256
# from unittest.mock import Mock, patch, MagicMock
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.test import APIClient
# from django.test import RequestFactory
# from django.db import IntegrityError
# from account.app.account.views import AccountCreate, AccountDestroy
# from account.app.account.serializers import AccountSerializer
# from account.app.account.services import create_account_number
# from account.app.account.models import Users, Account
#
#
# @pytest.fixture
# def mock_user_instance():
#     """Fixture for creating a mock user instance."""
#     return Mock(spec=Users, id='test_user_id')
#
# @pytest.fixture
# def account_instance(mock_user_instance):
#     """Fixture for creating a mock account instance."""
#     return Mock(spec=Account, id='12345678901234567890', balance=100.00, usernameid=mock_user_instance)
#
# @pytest.fixture
# def mock_account_serializer(account_instance):
#     """Fixture for creating a mock serializer."""
#     serializer_mock = Mock(spec=AccountSerializer)
#     serializer_mock.instance = account_instance
#     serializer_mock.is_valid.return_value = True
#     serializer_mock.save.return_value = account_instance
#     serializer_mock.data = {'id': account_instance.id, 'balance': '200.00', 'usernameid': account_instance.usernameid.id}
#     return serializer_mock
#
# @patch('account.app.account.models.Account.objects.filter')
# def test_create_account_number(mock_filter):
#     """Test checks the creation of an account number."""
#     mock_filter.return_value.exists.return_value = False
#     account_number = create_account_number()
#     assert len(account_number) == 20 and account_number.isdigit()
#     mock_filter.assert_called()
#
#
#
# def test_account_update_with_mocked_response(mock_account_serializer):
#     """Test checks account update with a mocked response."""
#     client = APIClient()
#     with patch('account.app.account.views.AccountUpdate', return_value=Response(
#             mock_account_serializer.data, status=status.HTTP_200_OK)) as mocked_put:
#         response = mocked_put(Mock(data={'balance': '200.00'}))
#         assert mocked_put.called
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == mock_account_serializer.data
#
# def test_account_destroy_with_mocked_response(account_instance):
#     """Test checks account deletion with a mocked response."""
#     with patch('account.app.account.views.AccountDestroy.get_object', return_value=account_instance), \
#          patch('account.app.account.views.AccountDestroy.perform_destroy', return_value=None):
#         view = AccountDestroy()
#         request = Mock()
#         view.setup(request, pk=account_instance.id)
#         response = view.delete(request, pk=account_instance.id)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#
# @pytest.fixture
# def user_data():
#     """Returns a dictionary with user data."""
#     return {
#         'email': 'test@example.com',
#         'full_names': 'Test User',
#         'id': 'test_id',
#         'password': 'password123',
#         'username': 'test_user'
#     }
#
# @pytest.fixture
# def account_data():
#     """Returns a dictionary with account data."""
#     return {
#         'id': 'test_account_id',
#         'balance': 100.00,
#         'usernameid': None  # You can replace None with a Users instance if needed
#     }
#
# def test_user_creation(user_data):
#     """Tests user creation."""
#     with patch('account.app.account.models.Users.objects.create') as mock_create:
#         Users.objects.create(**user_data)
#         mock_create.assert_called_once_with(**user_data)
#
# def test_unique_username_constraint(user_data):
#     """Tests that a username must be unique."""
#     with patch('account.app.account.models.Users.objects.create') as mock_create:
#         mock_create.side_effect = [None, IntegrityError()]
#         Users.objects.create(**user_data)  # Creating the first user
#         with pytest.raises(IntegrityError):
#             Users.objects.create(**user_data)  # Attempt to create a user with the same username
#
# def test_account_creation(account_data):
#     """Tests account creation."""
#     with patch('account.app.account.models.Account.objects.create') as mock_create:
#         Account.objects.create(**account_data)
#         mock_create.assert_called_once_with(**account_data)
#
# def test_account_balance_default():
#     """Tests that the default balance is correctly set."""
#     with patch('account.app.account.models.Account.objects.create') as mock_create:
#         mock_account_instance = MagicMock()
#         mock_account_instance.balance = 0
#         mock_create.return_value = mock_account_instance
#         account = Account.objects.create()
#         assert account.balance == 0
#
# def test_account_usernameid_null():
#     """Tests that usernameid is null by default."""
#     with patch('account.app.account.models.Account.objects.create') as mock_create:
#         mock_account_instance = MagicMock()
#         mock_account_instance.usernameid = None
#         mock_create.return_value = mock_account_instance
#         account = Account.objects.create()
#         assert account.usernameid is None
#
# def test_user_password_hashing(user_data):
#     """Tests password hashing for a user."""
#     with patch.object(Users, 'save', autospec=True) as mock_save:
#         user = Users(**user_data)
#         # Hashing the password before saving
#         user.password = sha256(user.password.encode('utf-8')).hexdigest()
#         user.save()
#         mock_save.assert_called_once()
#         # Verifying that the hashed password matches the expected hash
#         saved_password = user.password
#         expected_hashed_password = sha256(user_data['password'].encode('utf-8')).hexdigest()
#         assert saved_password == expected_hashed_password


from django.test import TestCase
from unittest.mock import patch, MagicMock

class ModelTestCase(TestCase):

    def setUp(self):
        # Мокирование методов менеджера модели Users
        self.users_objects_patch = patch('account.app.account.models.Users.objects', autospec=True)
        self.mock_users_objects = self.users_objects_patch.start()
        self.mock_users_objects.create = MagicMock()
        self.mock_users_objects.filter = MagicMock()
        self.mock_users_objects.get = MagicMock()
        self.mock_users_objects.all = MagicMock()
        self.mock_users_objects.update = MagicMock()
        self.mock_users_objects.delete = MagicMock()

        # Мокирование методов менеджера модели Account
        self.account_objects_patch = patch('account.app.account.models.Account.objects', autospec=True)
        self.mock_account_objects = self.account_objects_patch.start()
        self.mock_account_objects.create = MagicMock()
        self.mock_account_objects.filter = MagicMock()
        self.mock_account_objects.get = MagicMock()
        self.mock_account_objects.all = MagicMock()
        self.mock_account_objects.update = MagicMock()
        self.mock_account_objects.delete = MagicMock()

        # Мокирование методов экземпляра модели Account
        self.account_save_patch = patch('account.app.account.models.Account.save', MagicMock(name="save"), autospec=True)
        self.mock_account_save = self.account_save_patch.start()

    def tearDown(self):
        self.users_objects_patch.stop()
        self.account_objects_patch.stop()
        self.account_save_patch.stop()

    def test_user_creation(self):
        """
        Тест проверяет создание пользователя с мокированием зависимостей.
        """
        self.mock_generate_unique_id_number.return_value = 'unique_id_123'
        self.mock_make_password.return_value = 'hashed_password'
        mock_user = MagicMock(spec=Users)
        self.mock_users_manager.create.return_value = mock_user

        user_data = {
            "full_names": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "plainpassword"
        }

        # Имитация создания пользователя
        user = Users.objects.create(**user_data)

        self.mock_generate_unique_id_number.assert_called_once()
        self.mock_make_password.assert_called_once_with("plainpassword")
        self.mock_users_manager.create.assert_called_once_with(**user_data, password='hashed_password', id='unique_id_123')
        self.assertEqual(user, mock_user)

    def test_account_creation(self):
        """
        Тест проверяет создание аккаунта с мокированием зависимостей.
        """
        self.mock_generate_unique_id_number.return_value = 'account_id_123'
        mock_account = MagicMock(spec=Account)
        user_mock = MagicMock(spec=Users)
        self.mock_account_manager.create.return_value = mock_account

        account_data = {
            "balance": 100.00,
            "usernameid": user_mock
        }

        # Имитация создания аккаунта
        account = Account.objects.create(**account_data)

        self.mock_generate_unique_id_number.assert_called_once()
        self.mock_account_manager.create.assert_called_once_with(**account_data, id='account_id_123')
        self.assertEqual(account, mock_account)

    def test_balance_update(self):
        """
        Тест проверяет обновление баланса в модели Account без взаимодействия с базой данных.
        """
        account_mock = MagicMock(spec=Account, balance=100.00, usernameid=MagicMock(spec=Users))
        new_balance = 150.00
        account_mock.balance = new_balance

        account_mock.save()

        self.assertEqual(account_mock.balance, new_balance)
        account_mock.save.assert_called_once()
