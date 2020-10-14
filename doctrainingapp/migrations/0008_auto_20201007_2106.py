# Generated by Django 3.0.8 on 2020-10-08 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctrainingapp', '0007_conteudo_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conteudo',
            name='area',
        ),
        migrations.RemoveField(
            model_name='conteudo',
            name='imagem',
        ),
        migrations.AddField(
            model_name='conteudo',
            name='imagem1',
            field=models.ImageField(blank=True, null=True, upload_to='conteudo'),
        ),
        migrations.AddField(
            model_name='conteudo',
            name='imagem2',
            field=models.ImageField(blank=True, null=True, upload_to='conteudo'),
        ),
        migrations.AddField(
            model_name='conteudo',
            name='imagem3',
            field=models.ImageField(blank=True, null=True, upload_to='conteudo'),
        ),
    ]