from django_cte import CTEManager
from django.db.models import Avg, Min, Max, Count, Sum
from django.db.models.expressions import OuterRef, Subquery, F

from django_cte import With


from libreria.models.libros import Editorial, Libro


# Agrupado
def agrupar_libros_por_editorial():

    Libro.objects.values('editorial', 'editorial__nombre').annotate(
        total_libros=Count('isbn'))

    return consulta


def listado_editoriales():
    Editorial.objects.values('id', 'nombre')

# Usando subconsultas


def subconsulta_libros_por_editorial():

    total_libros_por_editorial = Libro.objects.values('editorial').annotate(
        total_libros=Count('isbn')).filter(editorial=OuterRef('id'))

    editoriales = Editorial.objects.values('id', 'nombre').annotate(
        total_libros=Subquery(total_libros_por_editorial.values('total_libros')))
    return editoriales

    # Cte usando el modelo principal


def cte_libros_por_editorial():

    total_libros = With(
        Libro.objects.values('editorial').annotate(
            total_libros=Count('isbn')), name='cuenta_libros'
    )

    editorial_totales = (
        total_libros
        .join(Editorial, id=total_libros.col.editorial_id)
        .with_cte(total_libros)
        .annotate(libros_editorial=total_libros.col.total_libros)
        .values('id', 'nombre', 'libros_editorial')
    )
    return editorial_totales

# Si no queremos poner el manejador CTEManager() en nuestro modelo principal


class LTManager(CTEManager):
    pass


class EditorialCustomManager(Editorial):
    class Meta:
        proxy = True
    objects = LTManager()


def cte_proxy_libros_por_editorial():
    total_libros = With(
        Libro.objects.values('editorial').annotate(
            total_libros=Count('isbn'), max_paginas=Max('paginas')), name="editorial_libros"
    )
    total_libros2 = With(
        Libro.objects.values('editorial').annotate(
            min_paginas=Min('paginas')), name="editorial_libros2"
    )

    # Usamos EditorialCustomManager en lugar del modelo original Editorial
    editorial_totales = (
        total_libros
        .join(
            total_libros2.join(
                EditorialCustomManager, id=total_libros2.col.editorial_id),
            id=total_libros.col.editorial_id)
        .with_cte(total_libros)
        .with_cte(total_libros2)
        .annotate(libros_editorial=total_libros.col.total_libros,
                  max_paginas=total_libros.col.max_paginas,
                  min_paginas=total_libros2.col.min_paginas
                  )
        .values('id', 'nombre', 'libros_editorial', 'max_paginas', 'min_paginas')
    )

    return editorial_totales


def cte_sencillo():
    cte = With(
        Libro.objects.values('editorial').annotate(
            total_libros=Count('isbn'), fecha_ultimo_libro=Max('fecha_publicacion'))
    )

    consulta = cte.queryset().with_cte(cte)
    return consulta


# class LT40QuerySet(CTEQuerySet):
#     def lt40(self):
#         return self.filter(paginas__gt=40)


# class LT30QuerySet(CTEQuerySet):

#     def lt30(self):
#         return self.filter(paginas__gt=30)


# class LT25QuerySet(CTEQuerySet):

#     def lt25(self):
#         return self.filter(paginas__gt=25)


# class LTManager(CTEManager):
#     pass


# class LibroFromLT40(Libro):
#     class Meta:
#         proxy = True
#     objects = CTEManager.from_queryset(LT40QuerySet)()


# class OrderLT40AsManager(Libro):
#     class Meta:
#         proxy = True
#     objects = LT40QuerySet.as_manager()


# class LibroCustomManagerNQuery(Libro):
#     class Meta:
#         proxy = True
#     objects = LTManager.from_queryset(LT25QuerySet)()


# class OrderCustomManager(Libro):
#     class Meta:
#         proxy = True
#     objects = LTManager()
