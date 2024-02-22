from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('full_names', 'username', 'email', 'password', 'id')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'username', 'password', 'full_names')

    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_names=validated_data.get('full_names', '')
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Users
        fields = ('email', 'username', 'password', 'full_names')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.full_names = validated_data.get('full_names', instance.full_names)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
