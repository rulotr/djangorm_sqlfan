
from django.db.models import CharField, Case, F, Q, Value as V, When
from django.db.models.functions import Concat, Left, Length, Replace


categorias = Libro.objects.all().select_related('editorial').filter(categoria__icontains='python')
for libro in categorias:
    print(libro.editorial.nombre)


consulta = Libro.objects.all().select_related('editorial').filter(categoria__contains='python')
dic_libros = dict(consulta.values_list('isbn','editorial__nombre'))
print(dic_libros)