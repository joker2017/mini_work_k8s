import random
import string
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND


# пример Account модели для использования в тестах
class Account:
    def __init__(self, id, balance, usernameid):
        self.id = id
        self.balance = balance
        self.usernameid = usernameid

# пример User модели для использования в тестах
class User:
    def __init__(self, id):
        self.id = id

# сериализатор для Account модели
class AccountSerializer(Serializer):
    def to_representation(self, instance):
        return {
            'balance': format(instance.balance, '.2f'),
            'id': instance.id,
            'usernameid': instance.usernameid,
        }

    class Meta:
        fields = ['balance', 'id', 'usernameid']

# функция для создания случайного id
def get_random_string(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

# функция для создания случайного номера счета
def create_account_number():
    return get_random_string(20, "0123456789")

# тестирование сериализатора AccountSerializer
class AccountSerializerTest(SimpleTestCase):
    def setUp(self):
        self.account = Account(
            id=1,
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

# тестирование функции create_account_number
class CreateAccountNumberTest(SimpleTestCase):
    def test_unique_account_number(self):
        account1 = User(id=get_random_string(20, "0123456789"))
        account2 = Account(id=get_random_string(20, "0123456789"))

        new_account_number = create_account_number()

        self.assertNotIn(new_account_number, [account1.id, account2.id])

    def test_account_number_length(self):
        new_account_number = create_account_number()

        self.assertEqual(len(new_account_number), 20)

# представление списка аккаунтов
class AccountList(APIView):
    def get(self, request):
        accounts = [
            Account(id=1, balance=100.0, usernameid='user1'),
            Account(id=2, balance=200.0, usernameid='user2'),
        ]
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# тестирование представления AccountList
class AccountListViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountList.as_view()

    def test_list_accounts(self):
        request = self.factory.get('/accounts/')
        response = self.view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_account(self):
        data = {
            'id': 3,
            'balance': 300.0,
            'usernameid': 'user3',
        }

        request = self.factory.post('/accounts/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        account = Account.objects.get(id=data['id'])
        serializer = AccountSerializer(account)

        self.assertEqual(response.data, serializer.data)

# представление создания аккаунта
class AccountCreate(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# представление обновления аккаунта
class AccountUpdate(APIView):
    def put(self, request, pk):
        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# представление деталей аккаунта
class AccountDetail(APIView):
    def get(self, request, usernameid):
        try:
            account = Account.objects.get(usernameid=usernameid)
        except Account.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account)
        return Response(serializer.data, status=HTTP_200_OK)

# представление удаления аккаунта
class AccountDestroy(APIView):
    def delete(self, request, pk):
        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        account.delete()
        return Response(status=HTTP_204_NO_CONTENT)

# тестирование представлений AccountCreate, AccountUpdate, AccountDetail, AccountDestroy
class AccountCreateViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountCreate.as_view()

    def test_create_account(self):
        data = {
            'id': 1,
            'balance': 100.0,
            'usernameid': 'user1',
        }

        request = self.factory.post('/accounts/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        account = Account.objects.get(id=data['id'])
        serializer = AccountSerializer(account)

        self.assertEqual(response.data, serializer.data)

class AccountUpdateViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountUpdate.as_view()

        self.account = Account(id=1, balance=100.0, usernameid='user1')

    def test_update_account(self):
        request = self.factory.put('/accounts/1/', data={'balance': 200.0}, format='json')
        response = self.view(request, pk=1)

        self.assertEqual(response.status_code, HTTP_200_OK)

        updated_account = Account.objects.get(id=1)
        self.assertEqual(updated_account.balance, 200.0)

    def test_update_nonexistent_account(self):
        request = self.factory.put('/accounts/2/', data={'balance': 200.0}, format='json')
        response = self.view(request, pk=2)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(id=2)

class AccountDetailViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountDetail.as_view()

        self.account = Account(id=1, balance=100.0, usernameid='user1')

    def test_get_account_detail(self):
        request = self.factory.get('/accounts/user1/')
        response = self.view(request, usernameid='user1')

        self.assertEqual(response.status_code, HTTP_200_OK)

        serializer = AccountSerializer(self.account)

        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_account_detail(self):
        request = self.factory.get('/accounts/nonexistent_username/')
        response = self.view(request, usernameid='nonexistent_username')

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

class AccountDestroyViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountDestroy.as_view()

        self.account = Account(id=1, balance=100.0)

    def test_destroy_account(self):
        request = self.factory.delete('/accounts/1/')
        response = self.view(request, pk=1)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(id=1)

    def test_destroy_nonexistent_account(self):
        request = self.factory.delete('/accounts/2/')
        response = self.view(request, pk=2)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)