# Generated by Django 2.2.5 on 2019-11-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctrainingapp', '0018_auto_20191107_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='nome_completo',
        ),
        migrations.AlterField(
            model_name='perfil',
            name='apelido',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]