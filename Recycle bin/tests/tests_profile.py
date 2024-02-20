import unittest
from unittest.mock import Mock
from ..views import UsersListView, UsersCreate, UsersUpdate, UsersDetail, UsersDestroy
from ..serializers import UsersSerializer
from django.test import SimpleTestCase
from rest_framework.response import Response

class UsersSerializerTest(unittest.TestCase):
    def test_serializer_fields(self):
        user_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword',
        }
        # Создаем экземпляр сериализатора с переданными данными пользователя
        serializer = UsersSerializer(data=user_data)
        
        self.assertTrue(serializer.is_valid())

        expected_fields = {'full_names', 'username', 'email', 'password', 'id'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

        self.assertTrue(serializer.fields['id'].read_only)


class UsersListViewTest(unittest.TestCase):
    def setUp(self):
        self.view = UsersListView()
        self.user1_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword1'
        }
        self.user2_data = {
            'full_names': 'Jane Smith',
            'username': 'janesmith',
            'email': 'janesmith@example.com',
            'password': 'securepassword2'
        }

    def test_list_users(self):
        users = [self.user1_data, self.user2_data]
        request = Mock()
        request.method = 'GET'
        request.GET = {}
        response = self.view.get(request)

        self.assertEqual(response.status_code, 200)

        expected_data = UsersSerializer(users, many=True).data
        self.assertEqual(response.data, expected_data)

    def test_search_users_by_full_names(self):
        request = Mock()
        request.method = 'GET'
        request.GET = {'search': 'John'}
        response = self.view.get(request)

        self.assertEqual(response.status_code, 200)

        users = [self.user1_data]
        expected_data = UsersSerializer(users, many=True).data
        self.assertEqual(response.data, expected_data)

    def test_search_users_by_username(self):
        request = Mock()
        request.method = 'GET'
        request.GET = {'search': 'janesmith'}
        response = self.view.get(request)

        self.assertEqual(response.status_code, 200)

        users = [self.user2_data]
        expected_data = UsersSerializer(users, many=True).data
        self.assertEqual(response.data, expected_data)


class UsersCreateViewTest(unittest.TestCase):
    def setUp(self):
        self.view = UsersCreate()
        self.user_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword1'
        }

    def test_create_user(self):
        request = Mock()
        request.method = 'POST'
        request.POST = self.user_data
        response = self.view.post(request)

        self.assertEqual(response.status_code, 201)

        created_user = {
            'id': 1,
            **self.user_data
        }
        expected_data = UsersSerializer(created_user).data

        self.assertEqual(response.data, expected_data)

    def test_create_user_with_invalid_data(self):
        request = Mock()
        request.method = 'POST'
        request.POST = {
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com'
        }
        response = self.view.post(request)

        self.assertEqual(response.status_code, 400)


class UsersUpdateViewTest(unittest.TestCase):
    def setUp(self):
        self.view = UsersUpdate()
        self.user_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword1'
        }
        self.user = self.user_data

    def test_update_user(self):
        request = Mock()
        request.method = 'PUT'
        request.PUT = {
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com',
            'password': 'newsecurepassword'
        }
        response = self.view.put(request, pk=self.user['id'])

        self.assertEqual(response.status_code, 200)

        updated_user = {
            'id': self.user['id'],
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com',
            'password': 'newsecurepassword'
        }
        expected_data = UsersSerializer(updated_user).data

        self.assertEqual(response.data, expected_data)
        self.assertEqual(self.user['full_names'], 'Jane Smith')
        self.assertEqual(self.user['email'], 'janesmith@example.com')
        self.assertEqual(self.user['password'], 'newsecurepassword')

    def test_update_nonexistent_user(self):
        request = Mock()
        request.method = 'PUT'
        request.PUT = {
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com',
            'password': 'newsecurepassword'
        }
        response = self.view.put(request, pk='nonexistent_id')

        self.assertEqual(response.status_code, 404)


class UsersDetailViewTest(unittest.TestCase):
    def setUp(self):
        self.view = UsersDetail()
        self.user_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword1'
        }
        self.user = self.user_data

    def test_get_user_detail(self):
        request = Mock()
        request.method = 'GET'
        response = self.view.get(request, id=self.user['id'])

        self.assertEqual(response.status_code, 200)

        expected_data = UsersSerializer(self.user).data

        self.assertEqual(response.data, expected_data)

    def test_get_nonexistent_user_detail(self):
        request = Mock()
        request.method = 'GET'
        response = self.view.get(request, id='nonexistent_id')

        self.assertEqual(response.status_code, 404)


class UsersDestroyViewTest(unittest.TestCase):
    def setUp(self):
        self.view = UsersDestroy()
        self.user_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword1'
        }
        self.user = self.user_data

    def test_destroy_user(self):
        request = Mock()
        request.method = 'DELETE'
        response = self.view.delete(request, pk=self.user['id'])

        self.assertEqual(response.status_code, 204)

        self.assertIsNone(self.user)

    def test_destroy_user_with_related_accounts(self):
        request = Mock()
        request.method = 'DELETE'
        response = self.view.delete(request, pk=self.user['id'])

        self.assertEqual(response.status_code, 403)

        self.assertIsNotNone(self.user)