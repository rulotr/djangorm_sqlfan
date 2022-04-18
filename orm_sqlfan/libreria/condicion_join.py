from django.db.models import Q, FilteredRelation
from libreria.models.libros import Editorial, Libro
from libreria.models import AutorCapitulo


def join_condicion_en_where():
    consulta = AutorCapitulo.objects.filter(
        libro__fecha_publicacion__year=2001).select_related(
        'libro').values('autor', 'libro__isbn', 'libro__titulo', 'libro__fecha_publicacion')

    return consulta
        

def left_join_condicion_en_where():
    consulta = AutorCapitulo.objects.filter(
        Q(libro__fecha_publicacion__year=2001) | Q(libro__fecha_publicacion=None)).select_related(
        'libro').values('autor', 'libro__isbn', 'libro__titulo', 'libro__fecha_publicacion')
    return consulta


def join_condicion_en_join():
    consulta = AutorCapitulo.objects.annotate(
        libro_pub2001=FilteredRelation('libro',
                                       condition=Q(libro__fecha_publicacion__year=2001))
    ).select_related('libro').values(
        'autor', 'libro_pub2001__isbn', 'libro_pub2001__titulo', 'libro_pub2001__fecha_publicacion')
    return consulta
