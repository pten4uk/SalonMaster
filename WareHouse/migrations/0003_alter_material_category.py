# Generated by Django 3.2.6 on 2021-09-08 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WareHouse', '0002_material_tracked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WareHouse.category', verbose_name='Категория'),
        ),
    ]
