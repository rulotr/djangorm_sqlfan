from libreria.models import Autor
from rest_framework import viewsets
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

class AutorSerializerBasico(serializers.ModelSerializer):
       class Meta:
        model = Autor
        fields = ['id', 'nombre']

class AutorViewSet(viewsets.ModelViewSet):
    serializer_class = AutorSerializerBasico
    queryset = Autor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'nombre': ['contains'],
    }