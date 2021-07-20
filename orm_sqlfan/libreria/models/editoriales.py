# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50, null=True)
    logo = models.ImageField(null=True,blank=True, default='', upload_to='fotos/')
    
    class Meta:
        managed = True
        db_table = 'libreria_editorial'
    
    def __str__(self):
        return f'Editoria {self.nombre}'

