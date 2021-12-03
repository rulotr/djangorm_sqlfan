from django.db.models import DecimalField, F, Q, Window, Value as V, DateField, ExpressionWrapper, F
from django.db.models.expressions import OuterRef, Subquery
from django.db.models.functions import RowNumber, Coalesce
from django_cte import CTEManager, With
from datetime import timedelta


from libreria.models import Libro, LibroPrecio, LibroPrecioCustomManager


def lista_precios_usando_subconsultas(fecha):
    libro_precios = LibroPrecio.objects.filter(libro=OuterRef(
        'isbn'), fecha_inicial__lte=fecha).order_by('-fecha_inicial')[:1]

    # libros = Libro.objects.values('isbn', 'titulo')
    libros = Libro.objects.annotate(
        el_precio=Subquery(libro_precios.values('precio'), output_field=DecimalField()))
    libros = libros.values('isbn', 'titulo', 'el_precio').filter(
        isbn__in=('1884777678', '1935182080', '1617291951'))

    return libros

# Anotar en la documentacion si queremos el orden descendente


class LTManager(CTEManager):
    pass


class LibroCustomManager(Libro):
    class Meta:
        proxy = True
    objects = LTManager()


def lista_precios_usando_funciones_de_ventana(fecha='2021-03-26'):
    ventana_conf = {'partition_by': [F('libro')],
                    'order_by': [F('fecha_inicial').desc()], }

    expresion_rownumber = Window(
        expression=RowNumber(), **ventana_conf)

    filtro = (LibroPrecioCustomManager.objects.annotate(
        col_num=expresion_rownumber,))
    filtro = filtro.filter(fecha_inicial__lte=fecha).values(
        'libro', 'fecha_inicial', 'precio', 'col_num')

    cte_precio_fecha = With(filtro, name='cte_precio_fecha')

    # consulta = cte_precio_fecha.queryset().with_cte(
    #    cte_precio_fecha).filter(col_num=1)

    consulta = (
        cte_precio_fecha
        .join(LibroCustomManager, isbn=cte_precio_fecha.col.libro_id)
        .with_cte(cte_precio_fecha)
        .annotate(precio=cte_precio_fecha.col.precio, num_fila=cte_precio_fecha.col.col_num)
        .filter(num_fila=1)
        .values('isbn', 'titulo', 'precio', 'num_fila')
    )

    return consulta


# Agregando la columna de fecha_final

# Pasos
# Agregar la columna fecha_final
# Realizar las migraciones

def consulta_lista_precios_usando_subconsultas():
    libro_fecha_final = LibroPrecio.objects.filter(libro=OuterRef(
        'libro_id'), fecha_inicial__gt=OuterRef('fecha_inicial')).order_by('fecha_inicial')[:1]

    consulta = LibroPrecio.objects.annotate(
        fecha_final_cal=Coalesce(Subquery(libro_fecha_final.values('fecha_inicial')), V('1900-01-01')))

    consulta = consulta.values(
        'libro_id', 'fecha_inicial', 'fecha_final', 'precio', 'fecha_final_cal')

    return consulta


def actualizar_lista_precios_usando_subconsultas():
    libro_fecha_final = LibroPrecio.objects.filter(libro=OuterRef(
        'libro_id'), fecha_inicial__gt=OuterRef('fecha_inicial')).order_by('fecha_inicial')[:1]

    libro_fecha_final = libro_fecha_final.annotate(fecha_menos_un_dia=ExpressionWrapper(
        F('fecha_inicial') - timedelta(days=1), output_field=DateField()
    ))

    LibroPrecio.objects.update(fecha_final=Coalesce(
        Subquery(libro_fecha_final.values('fecha_menos_un_dia')), V('1900-01-01')))


def lista_precios_con_columna_fecha_final(fecha='2021-03-26'):
    libros_precios = Libro.objects.annotate(
        fec_ini=F('libro_y_precios__fecha_inicial'),
        fec_fin=F('libro_y_precios__fecha_final')).select_related(
        'libro_y_precios').filter(
            (Q(fec_ini__lte=fecha, fec_fin__gte=fecha)
             |
             Q(fec_ini__lte=fecha, fec_fin=V('1900-01-01')))).values(
                 'isbn', 'titulo', 'libro_y_precios__precio', 'fec_ini', 'fec_fin')
    return libros_precios


def lista_precios_con_columna_fecha_final_corregida(fecha='2021-03-26'):
    relacion_nombre = 'libro_y_precios'
    fec_ini = f'{relacion_nombre}__fecha_inicial'
    fec_fin = f'{relacion_nombre}__fecha_final'
    fec_ini_lte = f'{fec_ini}__lte'
    fec_fin_gte = f'{fec_fin}__gte'

    query1 = Q()
    condicion1 = {fec_ini_lte: fecha, fec_fin_gte: fecha}
    condicion2 = {fec_ini_lte: fecha, fec_fin: V('1900-01-01')}
    query1 = Q(**condicion1)
    query1.add(Q(**condicion2), Q.OR)

    libros_precios = Libro.objects.select_related(relacion_nombre).filter(query1).values(
        'isbn', 'titulo', 'libro_y_precios__precio', fec_ini, fec_fin)
    return libros_precios
