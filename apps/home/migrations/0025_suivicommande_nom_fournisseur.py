# Generated by Django 3.1.14 on 2022-07-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_suivicommande'),
    ]

    operations = [
        migrations.AddField(
            model_name='suivicommande',
            name='nom_fournisseur',
            field=models.CharField(default='', max_length=64),
        ),
    ]
