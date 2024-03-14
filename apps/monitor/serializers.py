from rest_framework import serializers
from .models import UserForm, Portfolio, Language, LeadSupport


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


class LeadSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__',
