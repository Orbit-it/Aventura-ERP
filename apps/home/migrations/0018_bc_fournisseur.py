# Generated by Django 3.1.14 on 2022-07-18 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='BC_Fournisseur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier_commande', models.CharField(default='', max_length=64)),
                ('fournisseur_commande', models.CharField(default='', max_length=64)),
                ('numero_commande', models.CharField(default='', max_length=64)),
                ('article_commande', models.CharField(default='', max_length=30)),
                ('ref_stgi_commande', models.CharField(default='', max_length=30)),
                ('ref_fourn_commande', models.CharField(default='', max_length=30)),
                ('quantity_commande', models.FloatField(default=0)),
                ('pu_commande', models.FloatField(default=0)),
                ('unity_commande', models.CharField(default='PIECE', max_length=10)),
                ('prix_commande', models.FloatField(default=0)),
                ('prix_total_commande', models.FloatField(default=0)),
                ('rmq_commande', models.CharField(default='', max_length=300)),
                ('date_livraison_sht', models.DateField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]