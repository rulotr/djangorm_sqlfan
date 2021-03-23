# System
import io

#Django
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.db.models import Prefetch

#Others
from tabulate import tabulate

# Models
from libreria.models.editoriales import Editorial
from libreria.models.libros import Libro
from libreria.models.autores import Autor

#Serializers
from libreria.serializers import (EditorialSerializerBasico, 
            LibroSerializer, EditorialSerializerModel,
            LibroSerializer_Tipos, EditorialSerializerInverso,
            AutorSerializerProfundo)

# Serializacion Basica
def prueba_del_serializador_basico():
    editorial = Editorial.objects.get(pk=1)
    serializer = EditorialSerializerBasico(editorial)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    data = [[editorial,serializer,serializer.data,json]]
    print(tabulate(data, headers=["Modelo","Serializer","Serializer.Data","Json"]))
#endregion

# Deserializacion
def prueba_de_deserializacion():
    json =b'{"nombre":"Azteca", "pais":"Mexico"}'
    json_bytes = io.BytesIO(json)
    editorial_dic = JSONParser().parse(json_bytes)
    serializer = EditorialSerializerModel(data =editorial_dic)
    
    # Validando datos    
    is_valid = serializer.is_valid(raise_exception = True)
    errors = serializer.errors
    validated_data = serializer.validated_data
    #serializer.data
    #serializer.is_valid(raise_exception=True)
    # Convertir y guardar el modelo
    #editorial = Editorial()
    #editorial = serializer.save()
    editorial = Editorial(**validated_data)
        
    if is_valid:
        editorial.save()
    
    # Imprimir datos
    data1 = [[json,editorial_dic,serializer]]
    data2 = [[is_valid,errors,validated_data,editorial,editorial.nombre,editorial.id]]            
    print(tabulate(data1, headers=["Json","Dict","Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["is_valid","errors","validated_data","Modelo","Pais","Id","serializer.data"]))
#endregion

# Serializar un Modelo
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
#endregion

# Serializar varios libros
def prueba_del_serializador_modelo_lista():
    libro = Libro.objects.all()[:3].select_related('editorial')
    serializer = LibroSerializer(libro, many=True)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    data1 = [[serializer]]
    data2 = [[serializer.data]]
    data3 = [[json]]
    print(tabulate(data1, headers=["Serializer"]))
    print("\n")
    print(tabulate(data2, headers=["Serializer.Data"]))
    print("\n")
    print(tabulate(data3, headers=["Json"]))
#endregion

# Diferentes tipos de serializadores
def prueba_del_serializador_modelo_tipos():
    libro = Libro.objects.filter(isbn='1617290475').select_related('editorial').prefetch_related('libros_autores')
    serializer = LibroSerializer_Tipos(libro, context={'request': None}, many=True)    
    
    json = JSONRenderer().render(serializer.data)
    # Imprimir datos
    import json

    with open('editorial_libros.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)
#endregion

# Serializacion inversa
def prueba_editorial_inversa():
    editorial = Editorial.objects.all()[:3]
    serializer = EditorialSerializerInverso(editorial, many=True)    
    json = JSONRenderer().render(serializer.data)
    
    # Imprimir datos
    import json

    with open('editorial_libros.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)
#endregion

# Serializacion inversa de muchas editoriales
def prueba_editorial_inversa_muchos():
    editorial = Editorial.objects.filter(pk__in=(1,2)).prefetch_related('libro_editorial')

    serializer = EditorialSerializerInverso( editorial, many=True)    

    # Imprimir datos
    import json

    with open('editorial_libros.json', 'w') as file:
        json.dump(serializer.data, file, indent=1)
#endregion

# Serializacion profunda Autores - Libros - Editorial
def prueba_autores_libros_editorial():
        libro_y_editorial = Libro.objects.filter(titulo__contains='u').select_related('editorial')
        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related(
            Prefetch('libro', queryset=libro_y_editorial, to_attr='libaut'))

        serializer = AutorSerializerProfundo( autores, many=True)    
        # Imprimir datos
        import json

        with open('autor_libros_editorial.json', 'w') as file:
            json.dump(serializer.data, file, indent=1)
#endregion