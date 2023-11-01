from django.test import TestCase
from ..models import Account
from ..serializers import AccountSerializer


class AccountSerializerTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            balance=100.00,
            usernameid='testuser123',
        )

    def test_account_serialization(self):
        serializer = AccountSerializer(instance=self.account)

        self.assertEqual(serializer.data, {
            'balance': '100.00',
            'id': self.account.id,
            'usernameid': 'testuser123',
        })

    def test_account_deserialization(self):
        data = {
            'balance': '150.50',
            'id': 2,
            'usernameid': 'newuser456',
        }
        serializer = AccountSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_read_only_usernameid(self):
        serializer = AccountSerializer(instance=self.account)
        self.assertTrue('usernameid' in serializer.fields)
        self.assertTrue(serializer.fields['usernameid'].read_only)

    def test_valid_serializer_fields(self):
        self.assertEqual(AccountSerializer.Meta.fields, ['balance', 'id', 'usernameid'])
