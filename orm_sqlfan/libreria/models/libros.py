from django.db import models
from django.core.exceptions import ObjectDoesNotExist,ValidationError
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
        consulta = self.values('isbn','paginas').order_by('-paginas')[4]
        return consulta

    def los_cinco_libros_con_mas_paginas(self):
        consulta = self.values('isbn','paginas').order_by('-paginas')[0:5]
        return consulta


    def LibroPorPaginas(self, pagina):
        import math

        total_filas = self.count()
        filas_por_pagina = 5
        total_paginas = math.ceil(total_filas / filas_por_pagina)

        final = (pagina * filas_por_pagina)
        inicial = final - filas_por_pagina

        print(f'Pagina {pagina} / {total_paginas}')
        consulta = self.all().order_by('isbn')[inicial:final]
        return consulta

    def LibroPorPaginasDjango(self, pagina):
        from django.core.paginator import Paginator
        p = Paginator(self.all().order_by('isbn'), 5)
        print (f'Pagina {pagina} / {p.num_pages}')
        pag = p.page(pagina)
        return pag.object_list






def validar_titulo(titulo):
    if 'cobol' in titulo:
        raise ValidationError(f'{titulo} no se vende mucho')
    return titulo

class Libro(models.Model):
    estatus_libro = (('P', 'Publish'),('M','MEAP'))

    isbn = models.CharField(max_length=13, primary_key=True)
    titulo = models.CharField(max_length=70, blank=True, validators=[validar_titulo,])
    paginas = models.PositiveIntegerField()
    fecha_publicacion = models.DateField(null=True)
    imagen = models.URLField(max_length=85, null=True)
    desc_corta = models.CharField(max_length=2000, default='Sin reseña')
    estatus= models.CharField(max_length=1, choices=estatus_libro)
    categoria = models.CharField(max_length=50)

    edicion_anterior = models.ForeignKey('self', null=True, default=None, on_delete=models.PROTECT)

    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(titulo='cobol'), name='titulo_no_permitido_chk')]

    objects = LibroManager()

    def __str__(self):
        return self.isbn
