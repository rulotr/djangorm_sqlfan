from django.db import models

from .libros import Libro


class LibroCronica(models.Model):
    descripcion_larga = models.TextField(null=True)
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "%s Cronica del libro " % self.libro.isbn
