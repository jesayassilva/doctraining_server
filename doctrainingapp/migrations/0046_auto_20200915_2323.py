# Generated by Django 3.0.8 on 2020-09-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctrainingapp', '0045_fase_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fase',
            name='descricao',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]