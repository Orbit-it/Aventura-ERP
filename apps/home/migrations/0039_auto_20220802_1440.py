# Generated by Django 3.1.14 on 2022-08-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_remove_bc_fournisseur_date_livraison_sht'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bc_fournisseur',
            name='rmq',
        ),
        migrations.AddField(
            model_name='bc_fournisseur',
            name='date_livraison_sht',
            field=models.DateField(auto_now=True),
        ),
    ]
