from django.db import models

from libreria.models import Libro
from django_cte import CTEManager


class LibroPrecio(models.Model):
    libro = models.ForeignKey(
        Libro, on_delete=models.PROTECT, related_name='libro_y_precios')
    fecha_inicial = models.DateField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)

    fecha_final = models.DateField(null=True)


class LTManager(CTEManager):
    pass


class LibroPrecioCustomManager(LibroPrecio):
    class Meta:
        proxy = True
    objects = LTManager()
