# Los serializadores nos permiten convertir diferentes tipos de datos complejos
# a datos nativos de python los cuales podemos convertir a otros formatos
# como json o xml.
# Tambien podemos convertir los tipos de datos de python a datos complejos
# esto es lo que se llama deserializacion


# System
import io

#Django
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Models
from libreria.models.editoriales import Editorial
from libreria.models.libros import Libro

from tabulate import tabulate

# Serializacion Basica

class EditorialSerializerBasico(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    pais = serializers.CharField(max_length = 5)

def prueba_del_serializador():
    editorial = Editorial.objects.get(pk=1)
    serializer = EditorialSerializerBasico(editorial)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    data = [[editorial,serializer,serializer.data,json]]
    print(tabulate(data, headers=["Modelo","Serializer","Serializer.Data","Json"]))

def prueba_de_deserializacion():
    json =b'{"nombre":"Azteca","pais":"MX"}'
    json_bytes = io.BytesIO(json)
    libro_dic = JSONParser().parse(json_bytes)
    serializer = EditorialSerializerBasico(data =libro_dic)
    
    # Validando datos    
    is_valid = serializer.is_valid()
    errors = serializer.errors
    validated_data = serializer.validated_data
    #serializer.is_valid(raise_exception=True)
    
    # Convertir y guardar el modelo
    editorial = Editorial(**validated_data)
    editorial.save()
    
    # Imprimir datos
    data1 = [[json,libro_dic,serializer]]
    data2 = [[is_valid,errors,validated_data,editorial,editorial.pais,editorial.id]]            
    print(tabulate(data1, headers=["Json","Dict","Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["is_valid","errors","validated_data","Modelo","Pais","Id"]))
    
    
def prueba_de_deserializacion_parcial():
    json =b'{"pais":"Peru"}'
    json_bytes = io.BytesIO(json)
    libro_dic = JSONParser().parse(json_bytes)
    serializer = EditorialSerializerBasico(data =libro_dic,partial=True)
    
    # Validando datos    
    is_valid = serializer.is_valid()
    errors = serializer.errors
    validated_data = serializer.validated_data
    
    # Imprimir datos
    data1 = [[json,libro_dic,serializer]]
    data2 = [[is_valid,errors,validated_data]]            
    print(tabulate(data1, headers=["Json","Dict","Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["is_valid","errors","validated_data"]))
    
    # ModelSerializer

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'paginas','editorial']
        #fields = '__all__'
        #exclude = ['users']
        #depth=1

def prueba_del_serializador_modelo():
    libro = Libro.objects.get(isbn='1933988592')
    serializer = LibroSerializer(libro)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    data1 = [[libro,serializer]]
    data2 = [[serializer.data,json]]
    print(tabulate(data1, headers=["Modelo","Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["Serializer.Data","Json"]))

def prueba_del_serializador_modelo_lista():
    libro = Libro.objects.all()[:3]
    serializer = LibroSerializer(libro, many=True)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    data1 = [[libro,serializer]]
    data2 = [[serializer.data]]
    data3 = [[json]]
    print(tabulate(data1, headers=["Modelo","Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["Serializer.Data"]))
    print("\n")
    print(tabulate(data3, headers=["Json"]))

# Relaciones en los serializadores
class EditorialCustom(serializers.RelatedField):
    def to_representation(self, value):        
        return f'Mi editorial es {value.nombre} y soy de {value.pais}'


class LibroSerializer_Tipos(serializers.ModelSerializer):
    editorial1 = serializers.StringRelatedField(source='editorial')
    editorial2 = serializers.PrimaryKeyRelatedField(source='editorial',read_only=True)
    editorial3 = serializers.SlugRelatedField( source='editorial',slug_field='nombre',read_only=True)
    editorial4 = serializers.HyperlinkedRelatedField(source='editorial',view_name='editorial-detail',read_only=True)
    editorial5 = serializers.HyperlinkedIdentityField(source='editorial',view_name='editorial-detail',read_only=True)
    editorial6 = EditorialSerializerBasico(source='editorial')
    editorial7 = EditorialCustom(source='editorial',read_only=True)

    class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'paginas','editorial','editorial1','editorial2','editorial3','editorial4','editorial5','editorial6','editorial7']

class LibroSerializer_Hyper(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'paginas','editorial']


def prueba_del_serializador_modelo_tipos():
    libro = Libro.objects.get(isbn='1933988592')
    serializer = LibroSerializer_Tipos(libro, context={'request': None})    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    data1 = [[libro,serializer]]
    data2 = [[serializer.data]]
    data3 = [[json]]
    print(tabulate(data1, headers=["Modelo","Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["Serializer.Data"]))
    print("\n")
    print(tabulate(data3, headers=["Json"]))