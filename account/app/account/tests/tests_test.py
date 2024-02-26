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
from account.app.account.models import Users, Account

class ModelTestCase(TestCase):

    def setUp(self):
        # Мокирование методов и атрибутов модели Users
        self.patcher_users_create = patch('account.app.account.models.Users.objects.create')
        self.mock_users_create = self.patcher_users_create.start()

        self.patcher_generate_unique_id_number = patch('account.app.account.models.Users.generate_unique_id_number')
        self.mock_generate_unique_id_number = self.patcher_generate_unique_id_number.start()

        # Правильное мокирование функции make_password из Django
        self.patcher_make_password = patch('django.contrib.auth.hashers.make_password')
        self.mock_make_password = self.patcher_make_password.start()

        # Мокирование методов и атрибутов модели Account
        self.patcher_account_create = patch('account.app.account.models.Account.objects.create')
        self.mock_account_create = self.patcher_account_create.start()

        self.patcher_account_save = patch('account.app.account.models.Account.save', autospec=True)
        self.mock_account_save = self.patcher_account_save.start()

    def tearDown(self):
        self.patcher_users_create.stop()
        self.patcher_generate_unique_id_number.stop()
        self.patcher_make_password.stop()
        self.patcher_account_create.stop()
        self.patcher_account_save.stop()

    def test_user_creation(self):
        user_data = {
            "full_names": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "plainpassword"
        }
        mock_user = MagicMock(spec=Users)
        self.mock_users_create.return_value = mock_user
        self.mock_generate_unique_id_number.return_value = 'unique_id_123'
        self.mock_make_password.return_value = 'hashed_password'

        user = Users.objects.create(**user_data)

        self.mock_generate_unique_id_number.assert_called_once()
        self.mock_make_password.assert_called_once_with("plainpassword")
        self.mock_users_create.assert_called_once_with(**user_data, password='hashed_password', id='unique_id_123')
        self.assertEqual(user, mock_user)

    def test_account_creation(self):
        account_data = {
            "balance": 100.00,
            "usernameid": MagicMock(spec=Users)
        }
        mock_account = MagicMock(spec=Account)
        self.mock_account_create.return_value = mock_account
        self.mock_generate_unique_id_number.return_value = 'account_id_123'

        account = Account.objects.create(**account_data)

        self.mock_generate_unique_id_number.assert_called_once()
        self.mock_account_create.assert_called_once_with(**account_data, id='account_id_123')
        self.assertEqual(account, mock_account)

    def test_balance_update(self):
        mock_account = MagicMock(spec=Account, balance=100.00)
        new_balance = 150.00
        mock_account.balance = new_balance

        mock_account.save()

        self.assertEqual(mock_account.balance, new_balance)
        mock_account.save.assert_called_once()
