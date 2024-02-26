from .models import Account, Users
from .serializers import AccountSerializer
from rest_framework import generics, viewsets, mixins, filters




class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()  # Queryset that includes all users
    serializer_class = AccountSerializer  # Serializer class for user data
    filter_backends = [filters.SearchFilter]  # Backend filter for searching
    search_fields = ['=id', '=balance', 'usernameid__id']  # Fields to search against


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
