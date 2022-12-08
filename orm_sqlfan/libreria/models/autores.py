from django.db import models
from .libros import Libro

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=70)
    libro = models.ManyToManyField(Libro, through='AutorCapitulo', 
    related_name='libros_autores', through_fields=('autor','libro'))

    def __str__(self):
        return f'Yo soy {self.nombre}'
