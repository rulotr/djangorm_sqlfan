# Generated by Django 2.2.7 on 2022-07-18 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0021_auto_20210129_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='VLibroautores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(blank=True, max_length=13, null=True)),
                ('titulo', models.CharField(blank=True, max_length=70, null=True)),
                ('autores', models.TextField(blank=True, db_column='Autores', null=True)),
            ],
            options={
                'db_table': 'v_libroautores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LibroCalificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estrellas', models.PositiveIntegerField()),
                ('calificacion', models.CharField(blank=True, max_length=70)),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='libro_calificacion', to='libreria.Libro')),
            ],
        ),
    ]