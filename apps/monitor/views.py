from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import UserForm, Portfolio, Language
from .serializers import UserFormSerializer, PortfolioSerializer, LanguageSerializer
from rest_framework.filters import SearchFilter


class UserFormViewSet(viewsets.ModelViewSet):
    queryset = UserForm.objects.all()
    serializer_class = UserFormSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    filter_backends = [SearchFilter]
    search_fields = ['language']

    def get_queryset(self):
        queryset = super().get_queryset()
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)
        return queryset


class LanguageViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]
