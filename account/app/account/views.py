from .models import Account, Users
from .serializers import AccountSerializer, AccountSerializerRegistr
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

class AccountCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    API endpoint for creating a new account. Automatically generates
    a unique account number for each new account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializerRegistr

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Generate a unique account number
        id = create_account_number()
        serializer.save(id=id)
        headers = self.get_success_headers(serializer.data)
        # Return the newly created account details with a 201 status code
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AccountUpdate(generics.UpdateAPIView):
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


class AccountDestroy(generics.DestroyAPIView):
    """
    API endpoint for deleting an existing account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
