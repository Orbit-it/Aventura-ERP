# Generated by Django 3.1.14 on 2022-07-11 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_demande_identifier_demande'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimensionachat',
            name='identifier_dim',
            field=models.CharField(default='', max_length=64),
        ),
    ]