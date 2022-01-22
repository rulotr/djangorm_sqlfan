from django.db import models
from django.core.validators import MaxValueValidator
from .autores import Autor


class Calificacion(models.Model):
    estrellas = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)])
    comentario = models.CharField(
        max_length=2000, default='Sin comentarios')
    autor = models.ForeignKey(
        Autor, on_delete=models.PROTECT,
        related_name='autor_calificacion',)
