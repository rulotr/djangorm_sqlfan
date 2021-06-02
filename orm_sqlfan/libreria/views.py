from django.shortcuts import render, get_object_or_404

# Django Rest Framework
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions

#Models, Serializers
from .models import (Editorial, Libro)
from .serializers import (EditorialSerializerModel, LibroSerializer_Tipos,LibroSerializer)
# Create your views here.
from orm_sqlfan.exceptions import Excepcion_FaltanCampos

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

        editoriales = Editorial.objects.all()
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

#Vistas genericas

class EditorialListaGenericApiView(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset =Editorial.objects.all()
    serializer_class = EditorialSerializerModel

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        return self.create(request, *args, **kwargs)


class EditorialDetalleGenericApiView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset =Editorial.objects.all()
    serializer_class = EditorialSerializerModel

    def perform_destroy(self, instance):
        instance.pais ='Borrado Suave'
        instance.save()


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self,request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 
    
    def put(self, request, pk):
        return self.update(request, *args, **kwargs)

# Vistas concretas

class PaginacionLarga(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class EditorialListaConcretaGenericApiView(generics.ListAPIView,generics.CreateAPIView):
    queryset =Editorial.objects.all()
    serializer_class = EditorialSerializerModel
    pagination_class = PaginacionLarga


class EditorialListaMasConcretaGenericApiView(generics.ListCreateAPIView):
    queryset =Editorial.objects.all()
    serializer_class = EditorialSerializerModel

# Vista personalizada

class ListaFiltradaMixin:
    """
    List a queryset.
    Propiedades que usa pero no implementa
    busqueda_id
    busqueda_str
    """

    def mi_listado(self, request, *args, **kwargs):
        filtro = {}

        if("buscar" in self.request.query_params):
            valor = self.request.query_params['buscar']
            campo = self.busqueda_id if valor.isnumeric() else f'{self.busqueda_str}__contains'
            filtro[campo] = valor
            
        queryset = self.get_queryset().filter(**filtro)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return self.mi_listado(request, *args, **kwargs)

class EditorialListaCustomApiView(ListaFiltradaMixin, generics.GenericAPIView):
    queryset =Editorial.objects.all()
    serializer_class = EditorialSerializerModel
    busqueda_id = 'pk'
    busqueda_str = 'nombre'

    def get(self, request, *args, **kwargs):
        return self.mi_listado(request, *args, **kwargs)

class LibroListaCustomApiView(ListaFiltradaMixin, generics.GenericAPIView):
    queryset =Libro.objects.all().select_related('editorial')
    serializer_class = LibroSerializer
    busqueda_id = 'pk'
    busqueda_str = 'titulo'

    def get(self, request, *args, **kwargs):
        return self.mi_listado(request, *args, **kwargs)

# Vistas de conjunto


class EditorialViewSet(viewsets.ViewSet):
    def list(self, request):
        """
            Viendo las propiedades desde el metodo borrar
        """
        queryset = Editorial.objects.all()
        serializer = EditorialSerializerModel(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Editorial.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = EditorialSerializerModel(user)
        return Response(serializer.data)
    

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        """
            Viendo las propiedades desde el metodo borrar
        """
        propiedades = {}
        propiedades['basename'] = self.basename # Nombre base de la url que utilizara
        propiedades['action'] = self.action # La accion que realizara
        propiedades['detail'] = self.detail # Si es un detalle o un listado
        
        return Response(propiedades)


# Vistas Modelo de conjunto

class EditorialCortoViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel

    @action(detail=False)
    def ultimas_editoriales(self, request):
        ultimas_editoriales = Editorial.objects.all().order_by('-pk')[:5]

        serializer = self.get_serializer(ultimas_editoriales, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['post', 'delete'])
    def funcion_post_delete(self, request, pk=None):
       return Response('Hola soy otra accion')

class EditorialSoloLecturaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                ListaFiltradaMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel
    busqueda_id = 'pk'
    busqueda_str = 'nombre'

# Filtros

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters

class FiltroPaisNoNulo(filters.BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        return queryset.exclude(editorial__pais=None) 


class LibroConFiltros(generics.ListAPIView):

    #queryset =Libro.objects.all().select_related('editorial').filter(paginas__gt=0)
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, FiltroPaisNoNulo, filters.SearchFilter, filters.OrderingFilter]
    #filterset_fields = ['titulo','paginas','editorial__id']
    filterset_fields = {
        'paginas': ['gte','lte'],
        'titulo': ['contains'],
        'editorial__nombre': ['contains']
    }
    search_fields = ['titulo', 'editorial__nombre']
    ordering_fields = ['pk', 'titulo']
    ordering = ['pk']

    def get_queryset(self):
        queryset =Libro.objects.all().select_related('editorial')
        return queryset.filter(paginas__gt=0)
    

# Manejo de excepciones



class EditorialListaConExcepciones(APIView):    
    def get(self, request, format=None):
        editoriales = Editorial.objects.all()[:3]
        serializer = EditorialSerializerModel(editoriales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EditorialSerializerModel(data=request.data)
        
        if serializer.is_valid(raise_exception=False):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error = serializer.errors
        #error["NuevoError"] = "Este es nuevo"
        #raise exceptions.ValidationError(error)
        raise Excepcion_FaltanCampos()



