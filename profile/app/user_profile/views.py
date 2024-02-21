from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework import generics, viewsets, mixins, filters
from rest_framework.viewsets import GenericViewSet
#from .models import Users
from profile.app.user_profile.models import Users

from .serializers import UsersSerializer
from .services import create_account_number
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError

#https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/filtering
class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=full_names', '=username']

class UsersCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
         
        id = create_account_number()
        serializer.save(id=id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)  

class UsersUpdate(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_fields = 'id'
    def get_queryset(self):
        queryset = Users.objects.filter(id=self.kwargs['pk'])
        return queryset

class UsersDetail(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_fields = 'id'

    def get_queryset(self):
        return self.queryset.filter(
            id=self.kwargs['id'])

import pytest
from unittest.mock import patch, MagicMock
from django.db.models.deletion import ProtectedError
from rest_framework import status
from profile.app.user_profile.models import Users
from profile.app.user_profile.views import UsersDestroy

@pytest.fixture
def user_instance():
    # Создаем мок инстанс пользователя
    user = MagicMock(spec=Users)
    return user

@patch('profile.app.user_profile.models.Users.objects.get')
def test_user_destroy_with_protected_error(mock_get, user_instance):
    """
    Тест проверяет исключение при попытке удалить пользователя с привязанными к нему аккаунтами.
    """
    # Настройка мока
    mock_get.return_value = user_instance
    user_instance.delete.side_effect = ProtectedError("Нельзя удалить клиента с привязанными счетами")

    # Инициализация представления для удаления
    view = UsersDestroy()
    request = MagicMock()

    # Попытка удаления и проверка вызова исключения
    with pytest.raises(ProtectedError):
        view.destroy(request, pk=user_instance.id)

    # Проверяем, что мок метода delete был вызван
    user_instance.delete.assert_called_once()

    
