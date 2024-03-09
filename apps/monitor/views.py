from rest_framework import viewsets
from .models import UserForm
from .serializers import UserFormSerializer


class UserFormViewSet(viewsets.ModelViewSet):
    queryset = UserForm.objects.all()
    serializer_class = UserFormSerializer
