from rest_framework import viewsets
from .models import UserForm, Portfolio
from .serializers import UserFormSerializer, PortfolioSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter


class UserFormViewSet(viewsets.ModelViewSet):
    queryset = UserForm.objects.all()
    serializer_class = UserFormSerializer


class PortfolioListView(generics.ListAPIView):
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
