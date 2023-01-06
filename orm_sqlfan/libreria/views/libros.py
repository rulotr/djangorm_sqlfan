from rest_framework.response import Response
from libreria.models import Libro
from libreria.serializers import LibroSerializerBasico
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect, get_object_or_404
from django.http.response import JsonResponse

class LibroLista(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'libro/lista_libros.html'

    def get(self, request, format='json'):
        libros = Libro.objects.all()[0:5]
        serializer = LibroSerializerBasico(libros, many=True)
        return Response({'libros': libros})


class LibroDetalle(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name ='libro/detalle_libro.html'

    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializerBasico(libro)
        return Response({'libro':libro, 'serializer':serializer})

    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializerBasico(libro, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'libros': libro})
        serializer.save()
        return redirect('libro-lista')


class LibrosViewSet(viewsets.ModelViewSet):
    serializer_class = LibroSerializerBasico
    queryset = Libro.objects.all()