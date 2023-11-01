from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..models import Users, Account
from ..views import UsersListView, UsersCreate, UsersUpdate, UsersDetail, UsersDestroy
from ..serializers import UsersSerializer


class UsersListViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UsersListView.as_view()
        self.user1 = Users.objects.create(full_names='John Doe', username='johndoe', email='johndoe@example.com',
                                          password='securepassword1')
        self.user2 = Users.objects.create(full_names='Jane Smith', username='janesmith', email='janesmith@example.com',
                                          password='securepassword2')

    def test_list_users(self):
        request = self.factory.get('/api/users/')
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_search_users_by_full_names(self):
        request = self.factory.get('/usersearch/', {'search': 'John'})
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

        users = Users.objects.filter(full_names='John Doe')
        serializer = UsersSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_search_users_by_username(self):
        request = self.factory.get('/usersearch/', {'search': 'janesmith'})
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

        users = Users.objects.filter(username='janesmith')
        serializer = UsersSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)


class UsersCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UsersCreate.as_view()

    def test_create_user(self):
        data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword1'
        }

        request = self.factory.post('/usersearch/', data, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, 201)

        # Проверка, что пользователь был создан
        created_user = Users.objects.get(username='johndoe')
        serializer = UsersSerializer(created_user)
        self.assertEqual(response.data, serializer.data)

    def test_create_user_with_invalid_data(self):
        data = {
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com'
        }

        request = self.factory.post('/usersearch/', data, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, 400)


class UsersUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UsersUpdate.as_view()
        self.user = Users.objects.create(full_names='John Doe', username='johndoe', email='johndoe@example.com',
                                         password='securepassword1')

    def test_update_user(self):
        data = {
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com',
            'password': 'newsecurepassword'
        }

        request = self.factory.put(f'/profile2/{self.user.id}/', data, format='json')
        response = self.view(request, pk=self.user.id)

        self.assertEqual(response.status_code, 200)

        updated_user = Users.objects.get(id=self.user.id)
        serializer = UsersSerializer(updated_user)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(updated_user.full_names, 'Jane Smith')
        self.assertEqual(updated_user.email, 'janesmith@example.com')
        self.assertEqual(updated_user.password, 'newsecurepassword')

    def test_update_nonexistent_user(self):
        data = {
            'full_names': 'Jane Smith',
            'email': 'janesmith@example.com',
            'password': 'newsecurepassword'
        }

        request = self.factory.put('/api/users/nonexistent_id/', data, format='json')
        response = self.view(request, pk='nonexistent_id')

        self.assertEqual(response.status_code, 404)


class UsersDetailViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UsersDetail.as_view()
        self.user = Users.objects.create(full_names='John Doe', username='johndoe', email='johndoe@example.com',
                                         password='securepassword1')

    def test_get_user_detail(self):
        request = self.factory.get(f'/profile2/{self.user.id}/')
        response = self.view(request, id=self.user.id)

        self.assertEqual(response.status_code, 200)

        user = Users.objects.get(id=self.user.id)
        serializer = UsersSerializer(user)

        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_user_detail(self):
        request = self.factory.get('/profile2/nonexistent_id/')
        response = self.view(request, id='nonexistent_id')

        self.assertEqual(response.status_code, 404)


class UsersDestroyViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UsersDestroy.as_view()
        self.user = Users.objects.create(full_names='John Doe', username='johndoe', email='johndoe@example.com',
                                         password='securepassword1')

    def test_destroy_user(self):
        request = self.factory.delete(f'/profile2/{self.user.id}/')
        response = self.view(request, pk=self.user.id)

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Users.DoesNotExist):
            Users.objects.get(id=self.user.id)

    def test_destroy_user_with_related_accounts(self):
        request = self.factory.delete(f'/account/{self.user.id}/')
        response = self.view(request, pk=self.user.id)

        self.assertEqual(response.status_code, 403)

        self.assertTrue(Users.objects.filter(id=self.user.id).exists())
