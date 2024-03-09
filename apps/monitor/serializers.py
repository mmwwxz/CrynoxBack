from rest_framework import serializers
from .models import UserForm


class UserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserForm
        fields = ('name', 'phone', 'email')
