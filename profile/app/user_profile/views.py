from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework import generics, viewsets, mixins, filters
from rest_framework.viewsets import GenericViewSet
from .models import Users
from .serializers import UsersSerializer
from .services import create_account_number
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError
'''
class UserViewSet(#mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   #mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
'''



#https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/filtering
class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=full_names', '=username']

class UsersCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    #lookup_fields = 'usernameid'
    #lookup_url_kwargs = 'username'


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

    

class UsersDestroy(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_fields = 'id'

    def get_queryset(self):
        queryset = Users.objects.filter(id=self.kwargs['pk'])
        return queryset
           

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            return Response("Нельзя удалить клиента с привязхаными счетами", status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
