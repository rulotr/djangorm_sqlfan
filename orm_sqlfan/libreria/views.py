from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets

from libreria.models.editoriales import Editorial
from libreria.models.libros import Libro

from libreria.serializers import EditorialSerializerBasico,LibroSerializer_Hyper, LibroSerializerBasico
# Create your views here.

class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerBasico


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer_Hyper

