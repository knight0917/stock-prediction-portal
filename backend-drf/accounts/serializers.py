from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    class Meta:
        model=User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # User.objects.create will save the password in plain text.
        # User.objects.create_user will save the password in in hash(automatically).
        # user = User.objects.create_user(**validated_data) # this can be use only on if your fields is this three username, email, password.
        user= User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user


 