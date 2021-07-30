#Django
from rest_framework import serializers

# Models
from libreria.models.editoriales import Editorial
from libreria.models.libros import Libro
from libreria.models.autores import Autor

# Serializacion Basica

#region 
class EditorialSerializerBasico(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    pais = serializers.CharField(max_length = 5)
#endregion

#region
class EditorialSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id','nombre','pais']
#endregion

#region
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'paginas','editorial']
        #fields = '__all__'
        #exclude = ['users']
        depth=1
#endregion

# Relaciones en los serializadores

#region
class EditorialCustom(serializers.RelatedField):
    def to_representation(self, value):        
        return f'Mi editorial es {value.nombre} y soy de {value.pais}'
#endregion

#region
class LibroSerializer_Tipos(serializers.ModelSerializer):
    # Campos Serializadores
    titulo2 = serializers.CharField(source='titulo')

    # Serializadores de relacion
    editorial1 = serializers.StringRelatedField(source='editorial')
    editorial2 = serializers.PrimaryKeyRelatedField(source='editorial',read_only=True)
    editorial3 = serializers.SlugRelatedField(queryset=Autor.objects.all(),source='libros_autores',slug_field='nombre',many=True)
    editorial4 = serializers.HyperlinkedRelatedField(source='editorial',view_name='fv_editorial-detalle',read_only=True)
    editorial5 = serializers.HyperlinkedIdentityField(source='editorial',view_name='fv_editorial-detalle',read_only=True)
    editorial6 = EditorialSerializerModel(source='editorial')
    editorial7 = EditorialCustom(source='editorial',read_only=True)


    class Meta:
        model = Libro
        fields = ['isbn', 'titulo','titulo2', 'paginas','editorial','editorial1','editorial2','editorial3','editorial4','editorial5','editorial6','editorial7']
#endregion

#region
class LibroSerializerSencillo(serializers.ModelSerializer):
    
    class Meta:
        model = Libro
        fields = ['isbn']
#endregion

#region
class EditorialSerializerInverso(serializers.ModelSerializer):   
    libro = LibroSerializerSencillo(many=True, read_only=True, source='libro_editorial')
    class Meta:
        model = Editorial
        fields = ['nombre','pais','libro']
#endregion

#region
class LibroSerializerEditorial(serializers.ModelSerializer):
    editorial_datos = EditorialSerializerModel(source='editorial')

    class Meta:
        model = Libro
        fields = ['isbn','editorial_datos']
#endregion

#region
class AutorSerializerProfundo(serializers.ModelSerializer):
    libros = LibroSerializerEditorial(source='libaut', many=True)
    
    class Meta:
        model = Autor
        fields = ['nombre','libros']
#endregion

class LibroSerializerAgrupar(serializers.ModelSerializer):
    isbn = serializers.CharField(required=False)
    paginas = serializers.IntegerField(required=False)
    categoria = serializers.CharField(required=False)
    estatus = serializers.CharField(required=False)
    editorial = EditorialSerializerModel(required=False)

    editorial__nombre = serializers.CharField(required=False)
    editorial__id = serializers.IntegerField(required=False)
    edit_pais = serializers.CharField(source='editorial__pais',required=False)

    tot_libros = serializers.IntegerField(required=False)

    class Meta:
        model = Libro
        fields = ['isbn','categoria','estatus','editorial','paginas','tot_libros','editorial__id','editorial__nombre','edit_pais']


from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =('id','username','password','is_staff')
        extra_kwargs = {'password': {'write_only': True}}

