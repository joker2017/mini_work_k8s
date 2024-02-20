#import io

from rest_framework import serializers
from .models import Account 


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ('usernameid',)
        fields = ('balance', 'id', 'usernameid')

class AccountSerializerRegistr(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        fields = ('balance', 'id', 'usernameid')
