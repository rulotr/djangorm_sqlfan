# Generated by Django 2.2.7 on 2019-12-10 04:29

from django.db import migrations

def cargar_datos_desde_sql():
    from orm_sqlfan.settings import BASE_DIR
    import os
    sql_script = open(os.path.join(BASE_DIR,'libreria/sql/migracion.sql'),'r').read()
    return sql_script


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0016_autor_libro'),
    ]

    operations = [
        migrations.RunSQL(cargar_datos_desde_sql(),)
    ]
