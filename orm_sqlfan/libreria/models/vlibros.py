from django.db import models


class VLibroautores(models.Model):
    isbn = models.CharField(max_length=13, blank=True, null=True)
    titulo = models.CharField(max_length=70, blank=True, null=True)
    autores = models.TextField(db_column='Autores', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'v_libroautores'
