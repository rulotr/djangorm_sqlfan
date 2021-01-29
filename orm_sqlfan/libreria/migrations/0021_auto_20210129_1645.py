# Generated by Django 2.2.7 on 2021-01-29 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0020_auto_20210127_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='editorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='libro_editorial', to='libreria.Editorial'),
        ),
    ]
