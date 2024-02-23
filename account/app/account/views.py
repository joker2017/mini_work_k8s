from .models import Account, Users
from .serializers import AccountSerializer  #, AccountSerializerRegistr
from .services import create_account_number
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

class AccountList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    API endpoint that allows accounts to be viewed.
    """
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class AccountCreate(generics.CreateAPIView):

    """
    API endpoint for creating a new account. Automatically generates
    a unique account number for each new account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer   #Registr


class AccountUpdate(generics.UpdateAPIView, generics.RetrieveAPIView):
    """
    API endpoint for updating an existing account's details.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveAPIView):
    """
    API endpoint that retrieves the details of a specific account,
    filtering by the username ID associated with the account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDestroy(generics.DestroyAPIView, generics.RetrieveAPIView):
    """
    API endpoint for deleting an existing account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
