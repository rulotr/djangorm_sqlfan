# Generated by Django 2.2.7 on 2019-12-08 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0011_libro_editorial'),
    ]

    operations = [
        migrations.AddField(
            model_name='autor',
            name='libro',
            field=models.ManyToManyField(to='libreria.Libro'),
        ),
    ]