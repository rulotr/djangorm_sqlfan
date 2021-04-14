from django.shortcuts import render, get_object_or_404

# Django Rest Framework
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

#Models, Serializers
from .models import (Editorial, Libro)
from .serializers import (EditorialSerializerModel, LibroSerializer_Tipos)
# Create your views here.

# Vistas Basadas en funciones

@api_view(['GET'])
def fv_editorial_falsa(request, pk):
    if request.method == 'GET':
        print("Datos del request")
        print(request.data)
        print(request.user)
        print(request.method)
        print(request.query_params)

        return Response('Vista de la Editorial')



@api_view(['GET', 'POST'])
def fv_editorial_lista(request):
    if request.method == 'GET':
        editoriales = Editorial.objects.all()
        serializer = EditorialSerializerModel(editoriales, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = EditorialSerializerModel(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Convertir y guardar el modelo
            #serializer.save()
            editorial = Editorial(**validated_data)
            editorial.save()

            serializer_response = EditorialSerializerModel(editorial)    
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT', 'DELETE'])
def fv_editorial_detalle(request, pk):
    try:
        editorial = Editorial.objects.get(pk=pk)
    except Editorial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EditorialSerializerModel(editorial)
        return Response(serializer.data)

    if request.method == 'DELETE':
        editorial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        serializer = EditorialSerializerModel(editorial,data=request.data)

        if(serializer.is_valid()):
            #serializer.save()
            #editorial.nombre = serializer.validated_data['nombre']
            #editorial.pais = serializer.validated_data['pais']
            editorial = Editorial(**serializer.validated_data)
            editorial.pk = pk
            editorial.save(update_fields=['nombre','pais'])
            editorial = Editorial.objects.get(pk=pk)
            serializer_response  = EditorialSerializerModel(editorial)
            return Response(serializer.data)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def fv_libro_lista(request):
    if request.method == 'GET':
        libro = Libro.objects.filter(isbn__in=('1617290475','1933988592')).select_related('editorial').prefetch_related('libros_autores')
 
        serializer = LibroSerializer_Tipos(libro, many=True, context={'request': request})
        return Response(serializer.data)


# Vistas en basadas en clases


class EditorialListaApiView(APIView):

    def get(self, request):
        from django.core.paginator import Paginator 
        num_pag =request.query_params.get('num_page',1)        
        
        p = Paginator(Editorial.objects.all().order_by('pk'), 5 )
        pag = p.page(num_pag)
        editoriales = pag.object_list

        #editoriales = Editorial.objects.all()
        serializer = EditorialSerializerModel(editoriales, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EditorialSerializerModel(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Convertir y guardar el modelo
            #serializer.save()
            editorial = Editorial(**validated_data)
            editorial.save()

            serializer_response = EditorialSerializerModel(editorial)    
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditorialDetalleApiView(APIView):
    def get_object(self, pk):
        editorial = get_object_or_404(Editorial, pk=pk)
        return editorial

    def get(self, request, pk):
        editorial = self.get_object(pk)
        print(editorial)
        serializer = EditorialSerializerModel(editorial)
        return Response(serializer.data)
    
    def delete(self,request, pk):
        editorial = self.get_object(pk)
        editorial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        editorial = self.get_object(pk)

        serializer = EditorialSerializerModel(editorial,data=request.data)

        if(serializer.is_valid()):
            #serializer.save()
            #editorial.nombre = serializer.validated_data['nombre']
            #editorial.pais = serializer.validated_data['pais']
            editorial = Editorial(**serializer.validated_data)
            editorial.pk = pk
            editorial.save(update_fields=['nombre','pais'])
            editorial = Editorial.objects.get(pk=pk)
            serializer_response  = EditorialSerializerModel(editorial)
            return Response(serializer_response.data)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

