from django.db import models


class AutorCapitulo(models.Model):
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    numero_capitulos = models.IntegerField(default=0)


    def __str__(self):
        return f'Libro: {self.libro} Autor:{self.autor} Capitulos Escritos: {self.numero_capitulos}'
