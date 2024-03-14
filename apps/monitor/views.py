from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import UserForm, Portfolio, Language
from .serializers import UserFormSerializer, PortfolioSerializer, LanguageSerializer, LeadSupportSerializer
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


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


class LeadSupportView(APIView):
    def post(self, request, format=None):
        serializer = LeadSupportSerializer(data=request.data)
        if serializer.is_valid():
            print("Значение поля testing:", serializer.validated_data['testing'])
            print("Значение поля updating:", serializer.validated_data['updating'])

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)