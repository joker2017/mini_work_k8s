from rest_framework import generics, viewsets, mixins, filters
from .models import Users
from .serializers import UsersSerializer
from .services import create_account_number
from rest_framework.response import Response
from rest_framework import status
from django.db.models.deletion import ProtectedError


# View for listing users with search functionality
class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()  # Queryset that includes all users
    serializer_class = UsersSerializer  # Serializer class for user data
    filter_backends = [filters.SearchFilter]  # Backend filter for searching
    search_fields = ['=full_names', '=username']  # Fields to search against


# View for creating new users
class UsersCreate(generics.CreateAPIView):
    queryset = Users.objects.all()  # Queryset that includes all users
    serializer_class = UsersSerializer  # Serializer class for user data



# View for updating existing user data
class UsersUpdate(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Users.objects.all()  # Queryset that includes all users
    serializer_class = UsersSerializer  # Serializer class for user data


# View for retrieving detail of a specific user
class UsersDetail(generics.RetrieveAPIView):
    queryset = Users.objects.all()  # Queryset that includes all users
    serializer_class = UsersSerializer  # Serializer class for user data



# View for deleting a user
class UsersDestroy(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Users.objects.all()  # Queryset that includes all users
    serializer_class = UsersSerializer  # Serializer class for user data
    lookup_fields = 'id'  # Field to look up user


    def destroy(self, request, *args, **kwargs):
          instance = self.get_object()
          if instance.accounts.exists():
             # Связанные аккаунты существуют, возвращаем ошибку
             return Response({"detail": "Невозможно удалить пользователя с привязанными аккаунтами"}, status=status.HTTP_403_FORBIDDEN)

          # Если связанных аккаунтов нет, удаляем пользователя
          return super().destroy(request, *args, **kwargs)