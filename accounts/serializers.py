from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Serialziador para ver usuarios y sus roles
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined',
                  'course', 'gender', 'is_active')




class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'course', 'gender', 'password')


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
