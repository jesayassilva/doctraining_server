# Generated by Django 3.1.1 on 2020-09-23 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctrainingapp', '0003_areafase'),
    ]

    operations = [
        migrations.AddField(
            model_name='fase',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='doctrainingapp.areafase'),
            preserve_default=False,
        ),
    ]
