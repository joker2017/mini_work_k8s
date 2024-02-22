from rest_framework import serializers
from .models import Users


# Serializer for the Users model
class UsersSerializer(serializers.ModelSerializer):
    """
    A serializer for the Users model.

    This serializer transforms Users model instances into JSON format and
    validates incoming data for creating or updating Users instances.
    """

    class Meta:
        model = Users  # Specifies the model related to this serializer
        fields = ('full_names', 'username', 'email', 'password', 'id')  # Fields to include in the serialized output
        read_only_fields = ('id',)  # 'id' field is read-only and not included in input data for create/update operations
