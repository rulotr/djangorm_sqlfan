from django.shortcuts import get_object_or_404 

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import mixins, generics
from rest_framework import viewsets

from libreria.models import Editorial
from libreria.serializers import EditorialSerializerSencillo

# Funciones basadas en vistas

@api_view(['GET', 'POST'])
def editorial_list(request):
    if request.method == 'GET':
        editoriales = Editorial.objects.all()
        serializer = EditorialSerializerSencillo(editoriales, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EditorialSerializerSencillo(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Convertir y guardar el modelo
            editorial = Editorial(**validated_data)
            editorial.save()

            serializer2 = EditorialSerializerSencillo(editorial)    
           

            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def editorial_detail(request, pk):
    try:
        editorial = Editorial.objects.get(pk=pk)
    except Editorial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EditorialSerializerSencillo(editorial)
        return Response(serializer.data)

# Clases basadas en vistas

class EditorialLista(APIView):
    def get(self, request, format=None):
        editoriales = Editorial.objects.all()[:3]
        serializer = EditorialSerializerSencillo(editoriales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EditorialSerializerSencillo(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Convertir y guardar el modelo
            editorial = Editorial(**validated_data)
            editorial.save()

            serializer2 = EditorialSerializerSencillo(editorial)    


            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditorialDetails(APIView):
    def get_object(self, pk):
        editorial = get_object_or_404(Editorial, pk=pk)

    def get(self, request, pk, format=None):
        editorial = self.get_object(pk)
        serializer = EditorialSerializerSencillo(editorial)
        return Response(serializer.data)

# Vistas Genericas
# Django nos proporciona una serie de vistas prefabricadas para las tareas mas comunes

# Para ver la lista la podemos consultar aqui: http://www.cdrf.co/

# Mixins: Proporciona las acciones que se utilizan para el comportamiento basico de la vista

# Podemos mezclar los mixins en nuestras vistas para darle la utilidad que queremos

# GeneicAPIView extiende de APIView y agrega algunos comportamientos requeridos para las vistas

# Mixins
class EditorialListAPIView(
         mixins.ListModelMixin
        ,generics.GenericAPIView
        ):
    queryset = Editorial.objects.all() # Es el objeto que se usara en esta vista
    serializer_class = EditorialSerializerSencillo # Es la clase que se usara para serializar y decerializar asi como validar

    # get es proporcionado por GenericAPIView
    def get(self, request, *args, **kwargs):
        # consulta los datos del objeto
        # le especifica al serializador que devolvera una lista
        # retorna los datos
        return self.list(request, *args, **kwargs) 

    # post es proporcionado por GenericAPIView
    def post(self, request, *args, **kwargs):
        # serializa los datos que le llegan
        # valida los datos usando el serializador
        # guarda los datos usando el serializador
        # Regresa los datos con un 201_CREATED
        # Si existe un error lo lanzara
        return self.create(request, *args, **kwargs)


class EditorialDetailAPIView(
         mixins.RetrieveModelMixin
        ,mixins.UpdateModelMixin
        ,mixins.DestroyModelMixin
        ,generics.GenericAPIView
        ):
    queryset = Editorial.objects.all() # Es el objeto que se usara en esta vista
    serializer_class = EditorialSerializerSencillo # Es la clase que se usara para serializar y decerializar asi como validar

   
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        # no serializa, elimina el objeto usando el modelo
        return self.destroy(request, *args, **kwargs)

#Clases de vistas concretas

class EditorialCreateListView(generics.CreateAPIView,generics.ListAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerSencillo

class EditorialGetDeletePutListView(generics.RetrieveAPIView,generics.DestroyAPIView,generics.UpdateAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerSencillo

    def perform_destroy(self, instance):
        instance.pais ='Borrado Suave'
        instance.save()

    #def perform_update(self, serializer):


class EditorialListCreateAPIView(generics.ListCreateAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerSencillo

    def get_queryset(self):
        return Editorial.objects.exclude(pais=None)

    #Solo guarda los datos
    #Estos ya fueron validados por metodo create
    def perform_create(self, serializer):
        serializer.save(pais=self.request.data['pais'] + "**")


# Vistas personalizadas

class BusquedaPorDiferentesCamposMixin:
    def get_object(self):      
        filter = {}
        if(self.kwargs["buscar"].isnumeric()): 
            filter[self.busqueda_id] = self.kwargs["buscar"]
        else:
            filter[self.busqueda_str] = self.kwargs["buscar"]
        obj = get_object_or_404(self.queryset, **filter) 
        return obj

class EditorialPersonalizadoView(BusquedaPorDiferentesCamposMixin, generics.RetrieveAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerSencillo
    busqueda_id ='id'
    busqueda_str = 'nombre'

# ViewSets
# son clases parecidas a las clases view pero estas proporcionan read y update,create,list,retrieve por ejemplo en lugar
# de get y put
# Estas clases nos permiten realizar las interacciones del api y dejar que la gestion
# de las urls se gestione de manera automatica.

class EditorialExplicitoViewSet(viewsets.ViewSet):
    def list(self, request):
        """
            Viendo las propiedades desde el metodo borrar
        """
        queryset = Editorial.objects.all()
        serializer = EditorialSerializerSencillo(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Editorial.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = EditorialSerializerSencillo(user)
        return Response(serializer.data)
    
    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        """
            Viendo las propiedades desde el metodo borrar
        """
        propiedades = {}
        propiedades['basename'] = self.basename
        propiedades['action'] = self.action
        propiedades['detail'] = self.detail
        propiedades['suffix'] = self.suffix
        
        return Response(propiedades)
    


class EditorialCortoViewSet(viewsets.ModelViewSet):
    serializer_class = EditorialSerializerSencillo
    queryset = Editorial.objects.all()

    @action(detail=False)
    def ultimas_editoriales(self, request):
        ultimas_editoriales = Editorial.objects.all().order_by('-pk')[:5]

        serializer = self.get_serializer(ultimas_editoriales, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['post', 'delete'])
    def funcion_post_delete(self, request, pk=None):
       pass

class EditorialSoloLecturaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializerSencillo



# http://www.cdrf.co