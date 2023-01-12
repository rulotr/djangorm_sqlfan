# Los serializadores nos permiten convertir diferentes tipos de datos complejos
# a datos nativos de python los cuales podemos convertir a otros formatos
# como json o xml.
# Tambien podemos convertir los tipos de datos de python a datos complejos
# esto es lo que se llama deserializacion

# System
from datetime import datetime
from dis import pretty_flags
from email.policy import default
import io

#Django
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from django.db.models import Prefetch, F


# Models
from libreria.models.autores import Autor
from libreria.models.editoriales import Editorial
from libreria.models.libros import Libro,LibroCalificacion
from libreria.models.autor_capitulo import AutorCapitulo

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

45
class LibroSerializer_Tipos(serializers.ModelSerializer):
    editorial1 = serializers.StringRelatedField(source='editorial')
    editorial2 = serializers.PrimaryKeyRelatedField(source='editorial',read_only=True)
    editorial3 = serializers.SlugRelatedField( source='editorial',slug_field='nombre',read_only=True)
    editorial4 = serializers.HyperlinkedRelatedField(source='editorial',view_name='editorial-detail',read_only=True)
    editorial5 = serializers.HyperlinkedIdentityField(source='editorial',view_name='editorial-detail',read_only=True)
    editorial6 = EditorialSerializerBasico(source='editorial')
    editorial7 = EditorialCustom(read_only=True)

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
    import json
    with open('serializar_tipos.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)
    # Relaciones inversas


class EditorialSerializerSencillo(serializers.ModelSerializer):
    
    class Meta:
        model = Editorial
        fields = ['id','nombre','pais']


class LibroSerializerSencillo(serializers.ModelSerializer):
    #editorial =EditorialSerializerSencillo()
    
    class Meta:
        model = Libro
        fields = ['isbn']

class LibroCalificacionSerializerEjemplo(serializers.ModelSerializer):

    class Meta:
        model = LibroCalificacion
        fields = ['estrellas','calificacion']

class LibroSerializerEjemplo(serializers.ModelSerializer):
    calificaciones =LibroCalificacionSerializerEjemplo(many=True, source='libro_calificacion')
    
    class Meta:
        model = Libro
        fields = ['isbn','titulo','paginas','calificaciones']

class EditorialSerializerEjemplo(serializers.ModelSerializer):
    libro = LibroSerializerEjemplo(many =True, source='libro_editorial')
    #libro_lista_isbn =serializers.StringRelatedField(  source='libro_editorial',many=True)
    #libro_lista_titulo =serializers.SlugRelatedField( source='libro_editorial',slug_field='titulo',read_only=True, many=True)
   
    class Meta:
        model = Editorial
        fields = ['nombre','pais','libro']

def prueba_ejemplo_1():
    
    libro_y_librocapitulos = Libro.objects.filter(estatus='P').prefetch_related('libro_calificacion')
    editorial = Editorial.objects.filter(pk__in=(2,9)).prefetch_related(
        Prefetch('libro_editorial', queryset=libro_y_librocapitulos)   )

   
    serializer = EditorialSerializerEjemplo(editorial, many=True)
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    import json

    with open('editorial_ejemplo_3.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)


class LibroSerializerEjemplo2(serializers.ModelSerializer):
    #calificaciones =LibroCalificacionSerializerEjemplo(many=True, source='libro_calificacion')
    
    class Meta:
        model = Libro
        fields = ['isbn','titulo']


class EditorialSerializerEjemplo2(serializers.ModelSerializer):
    estrellas = serializers.IntegerField()

    class Meta:
        model = Editorial
        fields = ['nombre','pais','estrellas']

def prueba_ejemplo_2():
    editoriales = Editorial.objects.all().annotate(
        libro = F('libro_editorial__isbn'),
        calificacion_id =F('libro_editorial__libro_calificacion__id'),
        estrellas=F('libro_editorial__libro_calificacion__estrellas'),
        ).values(
            'id','nombre','pais','libro','libro_editorial__titulo',
    'estrellas','calificacion_id').filter(
        estrellas__gt=0,
        estrellas__isnull=False)

    print(editoriales)
    serializer = EditorialSerializerEjemplo2(editoriales, many=True)
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    import json

    with open('editorial_ejemplo_2.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)



class EditorialSerializerInverso(serializers.ModelSerializer):   
    libro = LibroSerializerSencillo(many=True, read_only=True, source='libro_editorial')
    class Meta:
        model = Editorial
        fields = ['nombre','pais','libro']

def prueba_editorial_inversa():
    editorial = Editorial.objects.get(pk=1)
    serializer = EditorialSerializerInverso(editorial)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    import json

    with open('editorial_libros.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)

def prueba_editorial_inversa_muchos():
    editorial = Editorial.objects.filter(pk__in=(1,2)).prefetch_related('libro_editorial')

    serializer = EditorialSerializerInverso( editorial, many=True)    

    # Imprimir datos
    import json

    with open('editorial_libros.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)

    #Libro.objects.all().values('editorial').annotate(NumeroLibros=Count('*'))

    #Editorial.objects.all()[:3].select_related('libro_editorial')
    #Libro.objects.all()[:3].select_related('editorial')
    #Libro.objects.all()[:3].prefetch_related('editorial')

class AutorSerializerProfundo(serializers.ModelSerializer):
    libros = LibroSerializerSencillo(source='libaut', many=True)
    
    class Meta:
        model = Autor
        fields = ['nombre','libros']


def prueba_autores_libros_editorial():
        libro_y_editorial = Libro.objects.filter(titulo__contains='u').select_related('editorial')
        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related(
            Prefetch('libro', queryset=libro_y_editorial, to_attr='libaut'))

        serializer = AutorSerializerProfundo( autores, many=True)    
        # Imprimir datos
        import json

        with open('autor_libros_editorial.json', 'w') as file:
            json.dump(serializer.data, file, indent=1)

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id','nombre']

class LibroSerializer(serializers.ModelSerializer):
    editorial = EditorialSerializer()

    class Meta:
      
        model = Libro
        fields = ['isbn','titulo','editorial']

def ejemplo_libro_editorial_select_related():
    libro_y_editorial = Libro.objects.filter(
        titulo__contains=' python ').select_related('editorial').only('isbn','titulo','editorial__id','editorial__nombre')
    serializer = LibroSerializer(libro_y_editorial, many= True)
    # Imprimir datos
    import json
    with open('libro_y_editorial.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)

class LibroSerializer2(serializers.ModelSerializer):
    class Meta: 
        model = Libro
        fields = ['isbn','titulo']



class EditorialSerializer2(serializers.ModelSerializer):
    libros = LibroSerializer2(many=True, source='lib_edit')
    class Meta:
        model = Editorial
        fields = ['id','nombre','libros']

from django.db import models
from django.db.models import Value as V, F, Q, Avg, Case, When, ExpressionWrapper
from django.db.models.functions import TruncDate,Cast, ExtractDay, Now,ExtractMonth, ExtractYear
from datetime import datetime, timedelta

def ejemplo_edad():
    #Libro.objects.annotate(edad= TruncDate(V('2020-08-03', output_field=models.DateField())) ).all().first().values('edad')
    now = datetime.now()

    edad= Libro.objects.annotate(
        fecha_act= V(now, output_field=models.DateField())
    ).annotate(fecha_nac= V('1979-09-2', output_field=models.DateField())        
    ).annotate(dias=ExpressionWrapper( F('fecha_act') - F('fecha_nac') ,
                    output_field=models.DurationField())
    ).annotate( edad1= ExtractYear('fecha_act') - ExtractYear(F('fecha_nac')) 
    ).annotate( edad_v= ExtractYear('fecha_act') - ExtractYear(F('fecha_nac')) -
         Case(
            When(Q(fecha_nac__month__gt=ExtractMonth('fecha_act')) | Q(fecha_nac__month= ExtractMonth('fecha_act'), fecha_nac__day__gt= ExtractDay('fecha_act'))  ,
                  then = V(1)) , 
            default=V(0),  
            output_field=models.IntegerField()
            )
    ).all(        
    ).values('fecha_publicacion','fecha_nac','fecha_act','dias','edad1','edad_v'
    ).first()
    print(edad)
    #college_students.annotate(avg_no_of_days=Avg( F('college_start_date') - F('school_passout_date') )

def ejemplo_editorial_libro_prefetch_related():
    # select_related() Permite realizar una sola consulta
    # prefetch_related() hace una consulta separada por cada modelo

    #libro_y_editorial = Libro.objectsa.all().select_related('editorial')

    #for libro in libro_y_editorial:

    #    print(f'El libro es {libro}')
    #    print(f'La editorial es {libro.editorial.nombre}')




    libro_y_calificaciones = Libro.objects.prefetch_related('libro_calificacion')

    for libro in libro_y_calificaciones:

        print(f'El libro es {libro}')
        for calificacion in libro.libro_calificacion.all():
            print(f'{calificacion.estrellas} estrellas Calif:{calificacion.calificacion}')

# html y Forms

class LibroSerializerBasico(serializers.ModelSerializer):
   class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'paginas','fecha_publicacion', 
        'editorial','imagen', 'desc_corta']
        read_only_fields = ['editorial']






    #   print(f'El libro es {libro["isbn"]}')
    #    print(f'El libro es {libro["libro_calificacion__estrellas"]}')

        #print(f'La editorial es {libro_calificacion__estrellas'}') '''

    



# filtro = {}
# filtro['id'] =18
# filtro['pais'] = None
# Editorial.objects.filter(**filtro) 

# query  = Q()
# buscar = ['an','ba','za']
# for valor in buscar:
#    query |= Q(nombre__contains=valor)
# query.connector = 'OR' 
# query1= Q(pais='Mexico') 
# query2 = Q()
# query2.add(query1,Q.AND)
# query2.add(query,Q.AND)
# Editorial.objects.filter(query2)


