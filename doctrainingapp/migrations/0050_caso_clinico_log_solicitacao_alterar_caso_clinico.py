# Generated by Django 3.1.1 on 2020-09-22 20:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctrainingapp', '0049_auto_20200922_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caso_Clinico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doenca_classificada', models.BooleanField(default=True)),
                ('doenca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='doctrainingapp.doenca')),
                ('falsa_doenca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='falsa_doenca', to='doctrainingapp.doenca')),
                ('sintomas', models.ManyToManyField(to='doctrainingapp.Sintoma')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitacao_Alterar_Caso_Clinico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doenca_classificada', models.BooleanField(default=True)),
                ('tipo_alteracao', models.PositiveIntegerField()),
                ('acao', models.PositiveIntegerField(default=2)),
                ('data_solicitacao', models.DateTimeField(default=datetime.datetime.now)),
                ('nome_novo_sintoma_modificado', models.CharField(blank=True, max_length=100, null=True)),
                ('nome_nova_doenca_modificada', models.CharField(blank=True, max_length=100, null=True)),
                ('caso_clinico_a_modificar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctrainingapp.caso_clinico')),
                ('nome_doenca_a_modificar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nome_doenca_a_modificar', to='doctrainingapp.doenca')),
                ('nome_sintoma_a_modificar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nome_sintoma_a_modificar', to='doctrainingapp.sintoma')),
                ('nova_doenca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctrainingapp.doenca')),
                ('novos_sintomas', models.ManyToManyField(to='doctrainingapp.Sintoma')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_solicitacao', models.DateTimeField()),
                ('doenca', models.CharField(max_length=100)),
                ('sintomas', models.TextField(blank=True)),
                ('nova_doenca', models.CharField(max_length=100)),
                ('novos_sintomas', models.TextField()),
                ('doenca_classificada', models.BooleanField(default=False)),
                ('tipo_alteracao', models.PositiveIntegerField()),
                ('aux_tipo_alteracao', models.CharField(max_length=100)),
                ('acao', models.PositiveIntegerField()),
                ('data_alteracao', models.DateTimeField(default=datetime.datetime.now)),
                ('avaliador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='avaliador', to=settings.AUTH_USER_MODEL)),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitante', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
