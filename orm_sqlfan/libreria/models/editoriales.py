# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_cte import CTEManager
from django.core.exceptions import ValidationError

def validar_nombre(nombre):
    es_valido = all(x.isalpha() or x.isspace() for x in nombre)
    if not es_valido:
        raise ValidationError(
            'El nombre solo puede contener letras o espacios')
    
class NombreCortoField(models.CharField):
    description = 'Es un campo para nombres cortos'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        super().__init__(*args, **kwargs)
        self.validators.append(validar_nombre)

    def deconstruct(self):
        # Es usado para las migraciones
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def get_prep_value(self, value):
        #Usado por campos como lo son DateField
        print('prep_value')
        value = super().get_prep_value(value)
        return value[::-1]

    def to_python(self, value):
        print('to_python')
        value = super().to_python(value)
        return value.strip()

    def from_db_value(self, value, expression, connection):
        print('from_db_value')
        if value is None:
            return value
        return value.upper()[::-1]

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_corto = NombreCortoField() 
    nombre_corto2  = NombreCortoField(default = '') 
    class Meta:
        managed = True
        db_table = 'libreria_editorial'

    objects = CTEManager()
