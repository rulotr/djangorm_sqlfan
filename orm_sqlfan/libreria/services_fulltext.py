from libreria.models.libros import Libro
from libreria.models.autores import Autor
from django_tabulate import tabulate_qs
from django.db.models import Q, F
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

def imprimir(func):
    print(tabulate_qs(func))


def busqueda_ilike():
    libros = Libro.objects.filter(titulo__icontains='netwo').values('isbn','titulo')
    imprimir(libros)

def busqueda_search_sin_resultado():
    libros = Libro.objects.filter(titulo__search='netwo').values('isbn','titulo')
    imprimir(libros)

def busqueda_search_con_resultado():
    libros = Libro.objects.filter(titulo__search='network').values('isbn','titulo')
    imprimir(libros)

# searchvector
def busqueda_searchvector():
    libros = Libro.objects.annotate(search=SearchVector('titulo',config='english')).filter(search='network').values('isbn','titulo','search')
    imprimir(libros)

def busqueda_searchvector_idioma_esp():
    libros = Libro.objects.annotate(search=SearchVector('titulo',config='spanish'),).filter(search='nade').values('isbn','titulo','search')
    imprimir(libros)

def busqueda_search_tsquery_varias_columnas():
    libros = (Libro.objects.annotate(search=SearchVector('titulo','desc_corta',config='english'))
        .filter(search='mapreduce').values('isbn','titulo','desc_corta','search'))
    print(libros)

# tsquey usando SearchQuery
def busqueda_search_searchquery_like():
    libros = (Libro.objects.annotate(search=SearchVector('titulo',config='english'),)
                            .filter(search=SearchQuery('netwo:*', search_type='raw')).values('isbn','titulo'))
    imprimir(libros)

def busqueda_search_searchquery_or():
    libros = (Libro.objects.annotate(search=SearchVector('titulo',config='english'),)
                            .filter(search=SearchQuery('program | programmer', search_type='raw')).values('isbn','titulo'))
    imprimir(libros)

def busqueda_search_searchquery_and():
    libros = (Libro.objects.annotate(search=SearchVector('titulo',config='english'),)
                            .filter(search=SearchQuery('program & network', search_type='raw')).values('isbn','titulo'))
    imprimir(libros)

def busqueda_search_searchquery_not():
    libros = (Libro.objects.annotate(search=SearchVector('titulo',config='english'),)
                            .filter(search=SearchQuery('!java & program', search_type='raw',config='english')).values('isbn','titulo'))
    imprimir(libros)

def busqueda_por_frases_columnavector():
    libros = (Libro.objects.filter(dsc_corta_token=SearchQuery('introduction', search_type='raw',config='english')).values('isbn','desc_corta'))
    print(libros)

# Busqueda de frases
def busqueda_por_frases_and():
    libros = (Libro.objects.filter(dsc_corta_token=SearchQuery('advance & features', search_type='raw',config='english')).values('isbn','desc_corta'))
    print(libros)

def busqueda_por_frases_juntas():
    libros = (Libro.objects.filter(dsc_corta_token=SearchQuery('advance <-> features', search_type='raw',config='english')).values('isbn','desc_corta'))
    print(libros)

def busqueda_por_frases_distancia():
    libros = (Libro.objects.filter(dsc_corta_token=SearchQuery('advance <2> features', search_type='raw',config='english')).values('isbn','desc_corta'))
    print(libros)

    
def busqueda_por_frases2():
    libros = (Libro.objects.filter(dsc_corta_token=SearchQuery('advance features', search_type='phrase',config='english')).values('isbn','desc_corta'))
    print(libros)

# La funcion de rango ts_rank pone un ranking de la busqueda 
# en funcion del numero de veces en que se encuentra cada termino
# la posicion dentro del documento
def busqueda_y_rango():
    query = SearchQuery('python',config='english')

    libros = (Libro.objects.annotate(
        rank=SearchRank("dsc_corta_token", query)
        )
        .filter(rank__gte=0.05)
        .order_by('-rank')).values('isbn','dsc_corta_token','rank',)
    print(libros)

# Busquedas de similaridad 
# Trigrams permite comparar dos cadenas y determinar que tan similares son,
# es como el quisiste decir de los buscadores

def busqueda_de_similaridad():
    autores =Autor.objects.annotate(similarity=TrigramSimilarity('nombre', 'salazar spencer'),).filter(nombre__contains='Salazar').values('nombre','similarity')
    print(autores)

def busqueda_de_similaridad2():
    autores =Autor.objects.annotate(similarity=TrigramSimilarity('nombre', 'maicol barlota'),).filter(similarity__gt=0.3).values('nombre','similarity')
    print(autores)

