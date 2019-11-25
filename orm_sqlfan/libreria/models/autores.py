from django.db import models

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=70)

    def __str__(self):
        return f'Yo soy {self.nombre}'
