from libreria.models.libros import Libro
from django_tabulate import tabulate_qs
from django.db.models import Q

def imprimir(func):
    print(tabulate_qs(func))


def libros_de_prueba():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        isbn__in=('161729134X', '132632942', '1933988495'))
    imprimir(libros)


def agregar_primer_detalle():
    libro = Libro.objects.get(isbn='1933988495')
    libro.detalles = {'genero': [
        'Programming', 'Python'], 'idioma': 'Ingles', 'Disponible': None, 
        'Estrellas': 5}
    libro.save()

    libro2 = Libro.objects.get(isbn='132632942')
    libro2.detalles = {'genero': ["Java", "Business"],
                       'idioma': 'Español', 'Disponible': 3}
    libro2.save()
    Libro.objects.filter(isbn='161729134X').update(
        detalles={'idioma': 'Español', 'BestSeller': True, 'Disponible': 4})


def consultas_none():
    libros = Libro.objects.values(
        'isbn', 'categoria', 'detalles').filter(detalles__Disponible=None)
    imprimir(libros)


def consultas_null():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        detalles__BestSeller__isnull=True,
        isbn__in=('161729134X', '132632942', '1933988495'))
    imprimir(libros)


def consulta_normal():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        detalles__idioma='Español')
    imprimir(libros)


# Podemos usar las consultas del orm vistas con anterioridad
def consulta_mayor_que():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        detalles__Disponible__gte=3)
    imprimir(libros)


def consulta_or():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        Q(detalles__BestSeller=True) | Q(detalles__idioma='Ingles'))
    imprimir(libros)


# O usar las consultas de contenido
def consulta_contains():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        detalles__contains={'idioma': 'Español'})
    imprimir(libros)


def consulta_contains2():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        detalles__contains={'idioma': 'Español', 'BestSeller': True})
    imprimir(libros)


def consulta_campo_contains_array():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
        detalles__genero__contains=['Python','Programming'])
    imprimir(libros)


def consulta_por_llave():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
           detalles__has_key='genero')
    imprimir(libros) 


def consulta_por_cualquier_llave():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
           detalles__has_any_keys=['BestSeller', 'Estrellas'])
    imprimir(libros) 


def consulta_por_todas_las_llaves():
    libros = Libro.objects.values('isbn', 'categoria', 'detalles').filter(
           detalles__has_keys=['genero', 'idioma', 'Disponible', 'Estrellas'])
    imprimir(libros)  

