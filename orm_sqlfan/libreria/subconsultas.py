from django.db.models import Count, IntegerField, FloatField, ExpressionWrapper, Sum, Min, Max, Avg
from django.db.models.expressions import OuterRef, Exists, OuterRef, Subquery, F
from libreria.models.autores import Autor
from libreria.models.editoriales import Editorial
from libreria.models.libros import Libro


def editoriales_con_mas_de_30_libros():
    editoriales = Editorial.objects.values('id').annotate(
        cantidad=Count('libro_editorial__isbn'))
    editoriales = editoriales.filter(cantidad__gte=40)
    return editoriales


def libros_de_las_editoriales_con_mas_de_30_libros_f1():
    editoriales = editoriales_con_mas_de_30_libros().values_list('id')
    libros = Libro.objects.filter(editorial__in=list(editoriales))
    return libros.values('isbn', 'titulo', 'editorial')


def libros_de_las_editoriales_con_mas_de_30_libros_f2():
    editoriales = editoriales_con_mas_de_30_libros().values('id')
    libros = Libro.objects.filter(editorial__in=editoriales)
    return libros.values('isbn', 'titulo', 'editorial')


# Subconsultas correlacionadas

def consulta_usando_subquery():
    editoriales = Editorial.objects.values('id')
    editoriales = editoriales.annotate(
        cantidad=Count('libro_editorial__isbn'))
    #editoriales = editoriales.filter(cantidad__gte=40)
    editoriales = editoriales.filter(id=OuterRef(
        'editorial_id'))

    num_autores = Autor.objects.values('libro__isbn').annotate(
        num_aut=Count('libro__isbn')).filter(
            libro__isbn=OuterRef('isbn')).values('num_aut')

    libros = Libro.objects.annotate(
        cant=Subquery(editoriales.values('cantidad'), output_field=IntegerField()))

    libros = libros.annotate(num_aut=Subquery(num_autores))

    libros = libros.filter(cant__gte=40).values(
        'isbn', 'editorial', 'cant', 'num_aut')
    return libros


def consulta_usando_exists():
    editoriales = Editorial.objects.values('id')
    editoriales = editoriales.filter(id=OuterRef(
        'editorial_id'))
    editoriales = editoriales.annotate(
        cantidad=Count('libro_editorial__isbn'))
    editoriales = editoriales.filter(cantidad__gte=40)
    libros = Libro.objects.annotate(
        cant=Exists(editoriales)).filter(cant=True)  # ~Exists
    libros = libros.values('isbn', 'editorial', 'cant')
    return libros


def consulta_usando_exists_y_subquery():
    editoriales = Editorial.objects.values('id')
    editoriales = editoriales.filter(id=OuterRef(
        'editorial_id'))
    editoriales = editoriales.annotate(
        cantidad=Count('libro_editorial__isbn'))

    editoriales = editoriales.filter(cantidad__gte=40)
    libros = Libro.objects.annotate(
        cant=Exists(editoriales)).annotate(
        cant_subq=Subquery(editoriales.values('cantidad'), output_field=IntegerField()))
    libros = libros.filter(cant=True)
    libros = libros.values('isbn', 'editorial', 'cant_subq')
    return libros
