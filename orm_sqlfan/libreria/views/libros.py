from libreria.models import Libro
from rest_framework import viewsets
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

class LibroSerializerBasico(serializers.ModelSerializer):
       class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'paginas','fecha_publicacion', 
        'editorial','imagen', 'desc_corta']
        read_only_fields = ['editorial']

class LibrosViewSet(viewsets.ModelViewSet):
    serializer_class = LibroSerializerBasico
    queryset = Libro.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'titulo': ['contains'],
    }