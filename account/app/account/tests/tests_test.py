from django.test import SimpleTestCase, override_settings
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from account.models import Account
from account.views import AccountList, AccountCreate, AccountUpdate, AccountDetail, AccountDestroy
from account.services import create_account_number
from account.serializers import AccountSerializer, AccountSerializerRegistr

# Мокирование модели Account для исключения обращения к БД
mock_account_qs = MagicMock()
mock_account = MagicMock(spec=Account)

# Тесты для API
@patch('account.models.Account.objects', mock_account_qs)
class AccountAPITestCase(APITestCase):
    def setUp(self):
        super().setUp()
        mock_account_qs.all.return_value = [mock_account]
        mock_account_qs.filter.return_value = mock_account_qs
        mock_account_qs.filter.return_value.exists.return_value = False

    @patch('account.views.AccountList.get_queryset', return_value=mock_account_qs.all())
    def test_account_list(self, mock_get_queryset):
        url = '/account/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('account.views.create_account_number')
    def test_account_create(self, mocked_create_account_number):
        mocked_create_account_number.return_value = '1234567890'
        url = '/account/create/'
        data = {'name': 'Test Account', 'balance': 1000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_account_update(self):
        pk = '123'
        url = f'/account/update/{pk}/'
        data = {'name': 'Updated Account', 'balance': 1500}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_account_detail(self):
        usernameid = 'testuser'
        url = f'/account/detail/{usernameid}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_account_destroy(self):
        pk = '123'
        url = f'/account/destroy/{pk}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

# Тесты для сервиса создания номера аккаунта и сериализаторов не требуют доступа к БД и могут использовать SimpleTestCase

@patch('account.services.Account.objects.filter')
class CreateAccountNumberTestCase(SimpleTestCase):
    def test_create_account_number_success(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        account_number = create_account_number()
        self.assertEqual(len(account_number), 20)
        self.assertTrue(account_number.isdigit())

    def test_create_account_number_retry(self, mock_filter):
        mock_filter.side_effect = [MagicMock(exists=MagicMock(return_value=True)),
                                   MagicMock(exists=MagicMock(return_value=False))]
        account_number = create_account_number()
        self.assertEqual(len(account_number), 20)
        self.assertTrue(account_number.isdigit())

class AccountSerializerTestCase(SimpleTestCase):
    def setUp(self):
        self.account_attributes = {
            'id': '12345678901234567890',
            'balance': '100.00',
            'usernameid': None
        }
        self.serializer_data = {
            'balance': '200.00',
            'id': '09876543210987654321',
            'usernameid': None
        }
        self.account = MagicMock(spec=Account, **self.account_attributes)

    def test_contains_expected_fields(self):
        serializer = AccountSerializer(instance=self.account)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['balance', 'id', 'usernameid']))

    def test_balance_field_content(self):
        serializer = AccountSerializer(instance=self.account)
        self.assertEqual(serializer.data['balance'], '100.00')

    @patch('account.serializers.AccountSerializerRegistr.save', MagicMock(name="save"))
    def test_account_save(self):
        serializer = AccountSerializerRegistr(data=self.serializer_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(AccountSerializerRegistr.save.called)
