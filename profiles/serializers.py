from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source='user.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='user.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='user.last_name',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ('id', 'user','first_name','last_name', 'bio',
                  'image','interest')
