#from typing_extensions import Required
from urllib import response
from django.http import HttpResponse
from fs import open_fs
import base64
from PyPDF2 import PdfFileReader, utils
import io
from django.db.models import Count, Sum, Max, Min
from orm_sqlfan.permissions import (
    EsGrupoAdministrador, EsGrupoRevisor, EsIpPermitida)
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters import rest_framework as filters
from django_filters import FilterSet, NumberFilter, DateFromToRangeFilter, BooleanFilter, CharFilter

from rest_framework.parsers import FileUploadParser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from django.contrib.auth import login
import requests
from djoser.conf import settings as django_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token
from copy import deepcopy
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissions)
from django.contrib.auth.models import User
from PIL import Image
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from rest_framework import serializers
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
import re
from django.shortcuts import render, get_object_or_404

# Django Rest Framework
from rest_framework import status, mixins, generics, viewsets
from rest_framework.fields import BooleanField, DateField
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions

#Models, Serializers
from .models import (Autor, Editorial, Libro, autor_capitulo, Calificacion)
from .serializers import (UsuarioSerializer, EditorialAutorSerializerModel, AutorSerializerModel, EditorialSerializerModel,
                          LibroSerializer_Tipos, LibroSerializer, LibroSerializerAgrupar, AutorConCalificacionesListadoSerializer,
                          AutorConCalificacionesSerializer
                          )
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
            # serializer.save()
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
        serializer = EditorialSerializerModel(editorial, data=request.data)

        if(serializer.is_valid()):
            # serializer.save()
            #editorial.nombre = serializer.validated_data['nombre']
            #editorial.pais = serializer.validated_data['pais']
            editorial = Editorial(**serializer.validated_data)
            editorial.pk = pk
            editorial.save(update_fields=['nombre', 'pais'])
            editorial = Editorial.objects.get(pk=pk)
            serializer_response = EditorialSerializerModel(editorial)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def fv_libro_lista(request):
    if request.method == 'GET':
        libro = Libro.objects.filter(isbn__in=('1617290475', '1933988592')).select_related(
            'editorial').prefetch_related('libros_autores')

        serializer = LibroSerializer_Tipos(
            libro, many=True, context={'request': request})
        return Response(serializer.data)


# Vistas en basadas en clases


class BinaryField(serializers.Field):
    def to_representation(self, value):
        return base64.b64decode(value.decode('utf-8'))

    def to_internal_value(self, value):
        return base64.b64encode(value.encode('utf-8'))


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        return "pdf"
    #     try:
    #         import ipdb
    #         ipdb.set_trace()
    #         PdfFileReader(io.BytesIO(decoded_file))
    #     except utils.PdfReadError as e:
    #         print(e)
    #     else:
    #         return 'pdf'


class LibroSerializerImage(serializers.ModelSerializer):
    archivo_pdf = BinaryField()

    class Meta:
        model = Libro
        fields = ['id', 'nombre', 'archivo_pdf']


class AutorApiView(APIView):
    def get(self, request):
        autores = Autor.objects.filter(pk__gte=576)
        serializer = AutorSerializerImage(autores, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_autor = AutorSerializerImage(
            data=request.data)

        if serializer_autor.is_valid():
            # Saco los datos del modelo Autor
            serializer_autor.save()

            return Response(serializer_autor.data, status=status.HTTP_201_CREATED)
        return Response(serializer_autor.errors, status=status.HTTP_400_BAD_REQUEST)


class LibroDetalleApiView(APIView):
    def get(self, request, pk):
        with open("media/Archivo.pdf", "rb") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Report.pdf"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                filename)

        return response


class EditorialListaApiView(APIView):

    def get(self, request):
        from django.core.paginator import Paginator
        num_pag = request.query_params.get('num_page', 1)

        p = Paginator(Editorial.objects.all().order_by('pk'), 5)
        pag = p.page(num_pag)
        editoriales = pag.object_list

        editoriales = Editorial.objects.all()
        serializer = EditorialSerializerModel(editoriales, many=True)
        return Response(serializer.data)

    def post(self, request):
        #{ "nombre": "PRUEBA 2", "pais": "Mexico 2", "autor": { "nombre": "Autor de prueba 2" }}
        # https://www.django-rest-framework.org/api-guide/serializers/
        serializer_editorial_autor = EditorialAutorSerializerModel(
            data=request.data)

        #serializer = EditorialSerializerModel(data=request.data)
        #serializer = AutorSerializerModel(data=request.data)
        if serializer_editorial_autor.is_valid():
            # Saco los datos del modelo Autor
            validate_editorial = serializer_editorial_autor.validated_data
            validate_autor = validate_editorial.pop(
                'autor')
            # Convertir y guardar el modelo
            # serializer.save()
            editorial = Editorial(**validate_editorial)
            editorial.save()
            autor = Autor(**validate_autor)
            autor.nombre = autor.nombre + ' ' + str(editorial.id)
            autor.save()
            serializer_response = AutorSerializerModel(editorial)

            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer_editorial_autor.errors, status=status.HTTP_400_BAD_REQUEST)


class EditorialDetalleApiView(APIView):
    def get_object(self, pk):
        editorial = get_object_or_404(Editorial, pk=pk)
        return editorial

    def get(self, request, pk):
        editorial = self.get_object(pk)
        print(editorial)
        serializer = EditorialSerializerModel(editorial)
        return Response(serializer.data)

    def delete(self, request, pk):
        editorial = self.get_object(pk)
        editorial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        editorial = self.get_object(pk)

        serializer = EditorialSerializerModel(editorial, data=request.data)

        if(serializer.is_valid()):
            # serializer.save()
            #editorial.nombre = serializer.validated_data['nombre']
            #editorial.pais = serializer.validated_data['pais']
            editorial = Editorial(**serializer.validated_data)
            editorial.pk = pk
            editorial.save(update_fields=['nombre', 'pais'])
            editorial = Editorial.objects.get(pk=pk)
            serializer_response = EditorialSerializerModel(editorial)
            return Response(serializer_response.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vistas genericas


class EditorialListaGenericApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        return self.create(request, *args, **kwargs)


class EditorialDetalleGenericApiView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                                     mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel

    def perform_destroy(self, instance):
        instance.pais = 'Borrado Suave'
        instance.save()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, pk):
        return self.update(request, *args, **kwargs)

# Vistas concretas


class PaginacionLarga(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class EditorialListaConcretaGenericApiView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel
    pagination_class = PaginacionLarga


class EditorialListaMasConcretaGenericApiView(generics.ListCreateAPIView):
    queryset = Editorial.objects.all()
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
            campo = self.busqueda_id if valor.isnumeric(
            ) else f'{self.busqueda_str}__contains'
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
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel
    busqueda_id = 'pk'
    busqueda_str = 'nombre'

    def get(self, request, *args, **kwargs):
        return self.mi_listado(request, *args, **kwargs)


class LibroListaCustomApiView(ListaFiltradaMixin, generics.GenericAPIView):
    queryset = Libro.objects.all().select_related('editorial')
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
        # Nombre base de la url que utilizara
        propiedades['basename'] = self.basename
        propiedades['action'] = self.action  # La accion que realizara
        propiedades['detail'] = self.detail  # Si es un detalle o un listado

        return Response(propiedades)


# Vistas Modelo de conjunto

#from rest_framework.permissions import DjangoObjectPermissions


class EditorialCortoViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerModel
    permission_classes = [IsAuthenticated]

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


class FiltroPaisNoNulo(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.exclude(editorial__pais=None)


class LibroConFiltros(generics.ListAPIView):

    #queryset =Libro.objects.all().select_related('editorial').filter(paginas__gt=0)
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, FiltroPaisNoNulo,
                       filters.SearchFilter, filters.OrderingFilter]
    #filterset_fields = ['titulo','paginas','editorial__id']
    filterset_fields = {
        'paginas': ['gte', 'lte'],
        'titulo': ['contains'],
        'editorial__nombre': ['contains']
    }
    search_fields = ['titulo', 'editorial__nombre']
    ordering_fields = ['pk', 'titulo']
    ordering = ['pk']

    def get_queryset(self):
        queryset = Libro.objects.all().select_related('editorial')
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

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error = serializer.errors
        #error["NuevoError"] = "Este es nuevo"
        #raise exceptions.ValidationError(error)
        raise Excepcion_FaltanCampos()


# Formas de subir una imagen o archivo


class EditorialSerializerImagenJson(serializers.ModelSerializer):
    logo = Base64ImageField(required=False)

    class Meta:
        model = Editorial
        fields = ['nombre', 'logo']


class EditorialImagenJson(APIView):
    def get(self, request, *args):
        print(str(self.parser_classes))
        return Response({'parsers': ' '.join(map(str, self.parser_classes))}, status=204)

    def post(self, request):
        serializer = EditorialSerializerImagenJson(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            archivo = validated_data['logo']
            archivo.name = 'mi_foto.png'
            validated_data['logo'] = archivo
            # Convertir y guardar el modelo
            editorial = Editorial(**validated_data)
            editorial.save()

            serializer_response = EditorialSerializerImagenJson(editorial)

            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Enviado por medio de HTML Form


class EditorialSerializerNormal(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['nombre', 'logo']


class EditorialImagenMultiParser(APIView):
    #parser_classes = (FormParser, MultiPartParser,)

    def post(self, request):
        if 'logo' not in request.data:
            raise exceptions.ParseError(
                "No has seleccionado el archivo a subir")

        archivos = str(request.FILES)

        #archivos = str(request.FILES.getlist('imagen1'))

        # return Response({'data':str(request.data),'file':archivos},status=status.HTTP_201_CREATED)
        serializer = EditorialSerializerNormal(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Convertir y guardar el modelo
            editorial = Editorial(**validated_data)
            editorial.save()

            serializer_response = EditorialSerializerNormal(editorial)

            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Enviar el archivo binario


class ImageParser(FileUploadParser):
    media_type = 'image/*'


class EditorialImagenFileUploadParser(APIView):
    parser_classes = (ImageParser,)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise exceptions.ParseError(
                "No has seleccionado el archivo a subir")

        archivo = request.data['file']
        try:
            img = Image.open(archivo)
            img.verify()
        except:
            raise exceptions.ParseError("El archivo no es una imagen")

        editorial = Editorial.objects.get(pk=1)
        # editorial.logo.save(archivo.name,archivo,save=True)
        editorial.logo.save('yolopuse.png', archivo, save=True)

        return Response({'data': str(request.data)}, status=status.HTTP_201_CREATED)

# Borrar una imagen


class EditorialBorrarImagen(APIView):
    def get_object(self, pk):
        editorial = get_object_or_404(Editorial, pk=pk)
        return editorial

    def delete(self, request, pk):
        editorial = self.get_object(pk)
        editorial.logo.delete(save=True)
        # editorial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Filtrado por agrupacion


class FiltroLibro(FilterSet):
    min_pag = NumberFilter(
        field_name='paginas', lookup_expr='gte', label='min_pag')
    #fecha_min = filters.DateFilter(field_name='fecha_publicacion', lookup_expr='gte', label='FecMin')
    fecha = DateFromToRangeFilter(field_name='fecha_publicacion')

    publicados = BooleanFilter(
        field_name='estatus', method='solo_publicados')

    agrupar_por = CharFilter(method='filtro_agrupado')

    def solo_publicados(self, queryset, name, value):
        valor = 'P' if value else 'M'
        return queryset.filter(estatus=valor)

    def filtro_agrupado(self, queryset, name, value):
        return queryset.values(*self.request.query_params.getlist('agrupar_por')).annotate(
            paginas=Sum('paginas'),
            tot_libros=Count('*')
        )

    class Meta:
        model: Libro
        fields = ['min_pag', 'fecha', 'tot_libros']


class LibroConFiltroAgrupado(generics.ListAPIView):
    serializer_class = LibroSerializerAgrupar
    filter_backends = [DjangoFilterBackend]
    filterset_class = FiltroLibro

    def get_queryset(self):
        queryset = Libro.objects.all().select_related('editorial')
        return queryset.filter(paginas__gt=0)


# Permisos listos para usar


# class CustomDjangoModelPermissions(DjangoModelPermissions):
#     view_permissions = ['%(app_label)s.view_%(model_name)s']

#     perms_map = {
#         'GET': view_permissions,
#         'OPTIONS': view_permissions,
#         'HEAD': view_permissions,
#         'POST': DjangoModelPermissions.perms_map['POST'],
#         'PUT': DjangoModelPermissions.perms_map['PUT'],
#         'PATCH': DjangoModelPermissions.perms_map['PATCH'],
#         'DELETE': DjangoModelPermissions.perms_map['DELETE'],
#     }


class CustomDjangoModelPermissions(DjangoModelPermissions):

    def __init__(self):
        self.perms_map = deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class UsuariosVista(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    #permission_classes = [IsAuthenticated]
    #permission_classes = [IsAuthenticatedOrReadOnly]
    #permission_classes = [IsAdminUser]
    #permission_classes = [DjangoModelPermissions]
    #permission_classes = [CustomDjangoModelPermissions]
    permission_classes = [EsGrupoRevisor | EsGrupoAdministrador]
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]

    def perform_create(self, serializer):
        usuario = serializer.save()
        usuario.set_password(usuario.password)
        usuario.save()

# Vista personalizada para el token


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# Djoser


class ActivateUserByGet(APIView):

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}
        protocol = 'https' if request.is_secure() else 'http'
        web_url = request.get_host()

        url = '{0}://{1}{2}'.format(protocol, web_url,
                                    reverse('user-activation'))
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({'detail': 'Activado de nuevo'})
        else:
            return Response(response.json())


# knox


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if request._auth is not None:
        print("Borrando token")
        request._auth.delete()
    print('Usuario entro')


# View Master/Detail

class AutorConCalificacionesApiView(APIView):
    def get(self, request):
        autores = Autor.objects.filter(
            pk__gte=578).prefetch_related('autor_calificacion')

        serializer = AutorConCalificacionesListadoSerializer(
            autores, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_autor_calificaciones = AutorConCalificacionesSerializer(
            data=request.data)

        # Validamos los datos a nivel modelo
        # Se validan tanto los del autor como los de las calificaciones
        if serializer_autor_calificaciones.is_valid():
            # Si los datos son validos separamos los datos
            # de autor y calificaciones
            resp_ser = serializer_autor_calificaciones.save()
            # Pasamos nuestro diccionario por el serializador
            serializer_response = AutorConCalificacionesSerializer(resp_ser)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)

        return Response(serializer_autor_calificaciones.errors, status=status.HTTP_400_BAD_REQUEST)

    def postObject(self, request):
        serializer_autor_calificaciones = AutorConCalificacionesSerializer(
            data=request.data)

        # Validamos los datos a nivel modelo
        # Se validan tanto los del autor como los de las calificaciones
        if serializer_autor_calificaciones.is_valid():
            # Si los datos son validos separamos los datos
            # de autor y calificaciones
            val_autor = serializer_autor_calificaciones.validated_data
            val_calificaciones = val_autor.pop('calificaciones')

            # Convertir y guardar el modelo Master (Autor)
            autor_nuevo = Autor(**val_autor)
            autor_nuevo.save()

            # Guardar los detalles (Calificaciones)
            calificaciones = []
            for calificacion_datos in val_calificaciones:
                calificacion_nueva = Calificacion.objects.create(
                    autor=autor_nuevo, **calificacion_datos)

                calificaciones.append(calificacion_nueva)

            # Armando un diccionario con los datos guardados
            dict_autor = autor_nuevo.__dict__
            dict_autor['calificaciones'] = calificaciones
            # Pasamos nuestro diccionario por el serializador
            serializer_response = AutorConCalificacionesSerializer(dict_autor)

            return Response(serializer_response.data, status=status.HTTP_201_CREATED)

        return Response(serializer_autor_calificaciones.errors, status=status.HTTP_400_BAD_REQUEST)
