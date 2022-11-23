from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import serializers, status

from .models import User
import re


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    def validate(self, data):
        strong_password_regex = "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
        if re.match(strong_password_regex, data["password"]):
            return data
        raise serializers.ValidationError({"password": "Your password must be secured\n"
                                                       "It should contain:\n"
                                                       "at least 1 letter\n"
                                                       "at least 1 number\n"
                                                       "at least 8 characters"})


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UsernameSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, request):
        # Take username and password from request
        response = {}
        username = request.get('username')
        password = request.get('password')

        if username and password:
            existing_user = User.objects.all().filter(username=username, password=password)
            if existing_user:
                response['user'] = existing_user.get()
                response['status'] = 200
                return response
            else:
                response['status'] = 404
                return response
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
