from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account model.

    This serializer is used to convert Account model instances into a JSON format
    and vice versa, making it easier to serialize and deserialize data for API requests
    and responses. It includes all model fields but sets 'usernameid' as read-only
    to prevent it from being modified through API operations.
    """
    class Meta:
        model = Account
        fields = ('balance', 'id')  # Explicitly specify fields to include
        read_only_fields = ('id',)  # 'usernameid' field should not be editable

#class AccountSerializerRegistr(serializers.ModelSerializer):


    #class Meta:
       # model = Account
       # fields = ('balance', 'id')  # Define fields to be included in the serialization
