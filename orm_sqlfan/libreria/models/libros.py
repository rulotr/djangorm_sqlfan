from django.db import models
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.db.models import Avg, Min, Max, Count, Sum
from django.db.models import CharField, Case, F, Q, Value as V, When
from django.db.models.functions import Concat, Left, Length, Replace
from django.db.models import Prefetch

from .editoriales import Editorial


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

    def __str__(self):
        return self.isbn
