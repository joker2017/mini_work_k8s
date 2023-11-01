from django.test import TestCase
from ..models import Users
from ..serializers import UsersSerializer


class UsersSerializerTest(TestCase):
    def test_serializer_fields(self):
        user_data = {
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'securepassword',
        }
        user = Users.objects.create(**user_data)

        serializer = UsersSerializer(instance=user)

        expected_fields = {'full_names', 'username', 'email', 'password', 'id'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

        self.assertTrue(serializer.fields['id'].read_only)
