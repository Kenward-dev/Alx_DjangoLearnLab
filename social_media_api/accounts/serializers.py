from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        ret['token'] = token.key
        return ret