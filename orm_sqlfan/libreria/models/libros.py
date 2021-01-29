from django.db import models
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.db.models import Avg, Min, Max, Count, Sum
from django.db.models import CharField, Case, F, Q, Value as V, When
from django.db.models.functions import Concat, Left, Length, Replace
from django.db.models import Prefetch

from .editoriales import Editorial


class LibroManager(models.Manager):
    def buscar_por_isbn(self, isbn):
        try:
            buscado = self.get(pk=isbn)
        except ObjectDoesNotExist:
            buscado = f'No existe el libro {isbn}'
        finally:
            return buscado

    def obtener_el_primer_libro(self):
        consulta = self.all().first()
        return consulta

    def obtener_el_ultimo_libro(self):
        consulta = self.all().last()

    def traer_con_limite_de_filas(self, filas):
        consulta =self.all()[:filas]
        return consulta

    def isbn_que_comienzan_por(self, isbn_buscar, **kwargs):
        consulta = self.filter(isbn__startswith=isbn_buscar, **kwargs)
        return consulta

    def libros_con_mas_de_200_paginas(self):
        consulta = self.filter(paginas__gt=200).exclude(isbn__in=('1933988592','1884777600')).order_by('paginas')
        return consulta

    def libros_con_mas_o_igual_a_200_paginas(self):
        consulta = self.filter(paginas__gte=200).filter(estatus='P').values('isbn','paginas').order_by('paginas')
        return consulta

    def cantidad_de_libros_con_menos_de_200_paginas(self):
        consulta =self.filter(paginas__lt=200).count()
        return consulta

    def Libros_con_200_paginas_O_con_300_paginas(self):
        consulta1 = self.filter(paginas=200)
        consulta2 =  self.filter(paginas=300)
        consulta = (consulta1 | consulta2).values('isbn','paginas')
        return consulta

    def Libros_publicados_en_el_año(self, año):
        consulta = self.filter(fecha_publicacion__year=año)
        return consulta.exists()

    def libros_con_isbn_correcto(self):
        consulta = self.filter(isbn__regex=r'19\d{8}$')
        return consulta

    def Autores_Editoriales_Hill(self):
        from .autores import Autor
        a1 = Autor.objects.filter(nombre__contains='hill').values('nombre')
        e1 = Editorial.objects.filter(nombre__contains='hill').values('nombre')
        consulta = a1.union(e1)
        return consulta

    def el_cuarto_libro_con_mas_paginas(self):
        consulta = self.values('isbn','paginas').order_by('-paginas')[3]
        return consulta

    def el_cuarto_y_quintoi_libro_con_mas_paginas(self):
        consulta = self.values('isbn','paginas').order_by('-paginas')[3:5]
        return consulta

    def LibroPorPaginas(self, pagina):
        import math

        total_filas = Libro.objects.count()
        filas_por_pagina = 5
        total_paginas = math.ceil(total_filas / filas_por_pagina)

        final = (pagina * filas_por_pagina)
        inicial = final - filas_por_pagina

        print(f'Pagina {pagina} / {total_paginas}')
        consulta = Libro.objects.all().order_by('isbn')[inicial:final]

        return consulta

    def LibroPorPaginasDjango(self,pagina):
        from django.core.paginator import Paginator
        p = Paginator(Libro.objects.all().order_by('isbn'), 5 )
        print(f'Pagina {pagina} / {p.num_pages}')
        pag = p.page(pagina)
        return pag.object_list

    # funciones de Agregacion Min, Max, Avg, Sum

    def minimo_paginas_para_un_libro(self):
        return self.filter(paginas__gt=0).aggregate(Min('paginas'))

    def maximo_paginas_para_un_libro(self):
        return self.filter(paginas__gt=0).aggregate(Max('paginas'))

    def numero_de_libros_de_python_agrupados_por_categoria(self):
        consulta = self.filter(categoria__contains='python').aggregate(Sum('paginas'))
        return consulta


    # Agrupaciones

    def numero_de_libros_de_python_agrupados_por_categoria(self):
        consulta = self.filter(categoria__contains='python').values('categoria').annotate(NumeroLibros=Count('*'), PromedioPaginas=Avg('paginas'), MinPaginas=Min('paginas'))
        return consulta

    def numero_de_libros_de_python_agrupados_por_categoria_y_editorial(self):
        consulta = self.filter(categoria__contains='python').values('categoria','editorial__nombre').annotate(NumeroLibros=Count('*'))
        # return consulta
        return consulta.filter(NumeroLibros__gt=1)

    def fechas_de_publicacion_con_mas_de_5_libros(self):
        consulta = self.values('fecha_publicacion').annotate(cant_fec_pub=Count('fecha_publicacion')).filter(cant_fec_pub__gte=5)
        return consulta

    def cuales_son_los_libros_de_la_consulta_anterior_forma1(self):
        consulta1 = self.fechas_de_publicacion_con_mas_de_5_libros()

        fechas_encontradas = [lib['fecha_publicacion'] for lib in consulta1]

        consulta = self.filter(fecha_publicacion__in= fechas_encontradas)
        return consulta

    def cuales_son_los_libros_de_la_consulta_anterior_forma2(self):
        consulta1 = self.fechas_de_publicacion_con_mas_de_5_libros().values_list('fecha_publicacion')
        consulta = self.filter(fecha_publicacion__in= consulta1).values('isbn')
        return consulta

    def distinct_de_paginas_menores_a_200(self):
        consulta = self.values('paginas').filter(paginas__lt=200).distinct()
        return consulta

    # Avanzadas

    def desc_corta_resumida(self):
        consulta = self.annotate(longitud = Length('desc_corta')).annotate(
            desc_resumida = Case(
                      When(longitud__gt=50, then = Concat(Left('desc_corta',50), V('...'))),
                      default=('desc_corta'),
                      output_field=CharField(),
                      )).filter(isbn__in=('1933988592','1884777791','1884777589','193239415X','1933988495')).values('isbn','desc_resumida','longitud')

        return consulta

    def titulo_inicia_igual_que_su_descripcion_corta(self):
        consulta = self.annotate(tit50= Left('titulo',50), desc50= Left('desc_corta',50)).filter(tit50 = F('desc50')).values('isbn','tit50','desc50')
        return consulta

    def mostrar_categoria_sin_comilla(self):
        consulta = self.annotate(categoria_sin_comillas = Replace('categoria', V('"'),V(''))).values('isbn','categoria','categoria_sin_comillas').filter(categoria__contains='python')
        return consulta

    def modfica_columna_categoria_quitando_corchetes(self):
        self.filter(categoria='[]').update(categoria = Replace('categoria', V('[]'),V('')))

    def libros_de_categoria_python_O_Java_O_net_version_corta(self):
        consulta = self.filter(Q(categoria__contains='python') | Q(categoria__contains='java') | Q(categoria__contains='net') & ~Q(paginas=0))
        return consulta

    def consulta_libros_con_cronica(self):
        consulta = self.select_related('librocronica').filter(categoria__contains='python')
        return consulta

    def consulta_libros_editorial_muchas_consultas(self):
        consulta = self.all().filter(categoria__contains='python')
        for libro in consulta:
            print(libro.editorial.nombre)
        return consulta

    def consulta_libros_editorial_muchas_consultas_forma2(self):
        consulta = self.all().select_related('editorial').filter(categoria__contains='python')
        for libro in consulta:
            print(libro.editorial.nombre)
        return consulta

    def consulta_libros_editorial_muchas_consultas_forma3(self):
        consulta = self.all().filter(categoria__contains='python')

        dic_libros = dict(consulta.values_list('isbn','editorial__nombre'))
        return dic_libros

# prefetch_related

    def autores_con_sus_libros_escritos_forma_inviable(self):
        from .autores import Autor
        autores = Autor.objects.filter(pk__in=(398,523))
        for autor in autores:
            print(f'Autor: {autor}')
            print('Libros escritos:')
            for libro in autor.libro.all():
                print(libro.titulo)

    def autores_con_sus_libros_escritos_forma_optima(self):
        from .autores import Autor
        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related('libro')
        for autor in autores:
            print(f'Autor: {autor}')
            print('Libros escritos:')
            for libro in autor.libro.all():
                print(libro.titulo)

    def autores_con_sus_libros_escritos_y_editoriales_forma_inviable(self):
        from .autores import Autor
        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related('libro')
        for autor in autores:
            print(f'Autor: {autor}')
            print('Libros escritos:')
            for libro in autor.libro.all():
                print(f'{libro.isbn} Editorial: {libro.editorial.nombre}')

    def autores_con_sus_libros_escritos_y_editoriales_forma_optima(self):
        from .autores import Autor
        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related('libro__editorial')
        for autor in autores:
            print(f'Autor: {autor}')
            print('Libros escritos:')
            for libro in autor.libro.all():
                print(f'{libro.isbn} Editorial: {libro.editorial.nombre}')

    def autores_con_sus_libros_escritos_y_editoriales_usando_prefecth(self):
        from .autores import Autor

        libro_y_editorial = Libro.objects.select_related('editorial')

        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related(
            Prefetch('libro', queryset=libro_y_editorial))

        for autor in autores:
            print(f'Autor: {autor}')
            print('Libros escritos:')
            for libro in autor.libro.all():
                print(f'{libro.isbn} Editorial: {libro.editorial.nombre}')


    def autores_con_sus_libros_escritos_y_editoriales_usando_prefecth_con_atributo(self):
        from .autores import Autor

        libro_y_editorial = Libro.objects.filter(titulo__contains='u').select_related('editorial')

        autores = Autor.objects.filter(pk__in=(398,523)).prefetch_related(
            Prefetch('libro', queryset=libro_y_editorial, to_attr='libaut'))

        for autor in autores:
            print(f'Autor: {autor}')
            print('Libros escritos:')
            for libro in autor.libaut:
                print(f'{libro.isbn} Editorial: {libro.editorial.nombre}')

   # Relacion inversa Libros - Autores
    def libros_con_sus_autores_y_su_editorial_optima(self):
        libros = self.filter(isbn__in=('1617290475', '1935182048')).select_related('editorial').prefetch_related('libros_autores')

        for p in libros:
            print(f'{p.isbn} - {p.titulo} Editorial: {p.editorial.nombre}  Escrito por:')
            for q in p.libros_autores.all():
                print(f'{q.nombre} ')



def validar_titulo(titulo):
    if 'cobol' in titulo:
        raise ValidationError(f'{titulo} no se vende mucho')
    return titulo

class Libro(models.Model):
    estatus_libro = (('P', 'Publish'),('M','MEAP'))

    isbn = models.CharField(max_length=13, primary_key=True)
    titulo = models.CharField(max_length=70, blank=True, validators=[validar_titulo,])
    paginas = models.PositiveIntegerField(db_index=True,)
    fecha_publicacion = models.DateField(null=True)
    imagen = models.URLField(max_length=85, null=True)
    desc_corta = models.CharField(max_length=2000, default='Sin reseña')
    estatus= models.CharField(max_length=1, choices=estatus_libro)
    categoria = models.CharField(max_length=50)

    edicion_anterior = models.ForeignKey('self', null=True, default=None, on_delete=models.PROTECT)

    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT, related_name='libro_editorial',)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(titulo='cobol'), name='titulo_no_permitido_chk')]

    objects = LibroManager()

    def __str__(self):
        return self.isbn
