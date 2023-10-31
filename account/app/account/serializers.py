#import io

from rest_framework import serializers
from .models import Account 


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        #fields = ("title", "content", "cat")
        #lookup_fields = lookup_fields = 'usernameid'
        read_only_fields = ('usernameid',)
        fields = ('balance', 'id', 'usernameid')
        #extra_kwargs = {
        #    'url': {'look_field': 'username'}
        #}

class AccountSerializerRegistr(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        #fields = ("title", "content", "cat")
        #lookup_fields = lookup_fields = 'usernameid'
        #read_only_fields = ('usernameid',)
        fields = ('balance', 'id', 'usernameid')
        #extra_kwargs = {
        #    'url': {'look_field': 'username'}
        #}
