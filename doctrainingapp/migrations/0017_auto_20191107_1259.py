# Generated by Django 2.2.5 on 2019-11-07 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctrainingapp', '0016_auto_20191107_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pergunta',
            name='opcao_correta',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='opcao_incorreta_1',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='opcao_incorreta_2',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='opcao_incorreta_3',
            field=models.CharField(max_length=600),
        ),
    ]
