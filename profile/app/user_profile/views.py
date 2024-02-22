from rest_framework import generics, viewsets, mixins, filters
from .models import Users
from .serializers import UsersSerializer, UserUpdateSerializer, UserCreateSerializer
from .services import create_account_number
from rest_framework.response import Response
from rest_framework import status
from django.db.models.deletion import ProtectedError


# View for listing users with search functionality
# Допустим, импорты выполнены корректно

class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=full_names', '=username']

class UsersCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer

class UsersUpdate(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'

class UsersDetail(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'id'

class UsersDestroy(generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the instance to be deleted

        try:
            self.perform_destroy(instance)  # Attempt to delete the instance
        except ProtectedError as e:
            # Return error response if instance cannot be deleted due to protected error
            return Response("Cannot delete the client with attached accounts", status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return success response for deletion
