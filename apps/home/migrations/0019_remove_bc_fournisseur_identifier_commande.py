# Generated by Django 3.1.14 on 2022-07-18 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_bc_fournisseur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bc_fournisseur',
            name='identifier_commande',
        ),
    ]
