from .models import Language
from rest_framework import serializers
from .models import UserForm, Portfolio


class UserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserForm
        fields = ('name', 'phone', 'email')


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = 'name',