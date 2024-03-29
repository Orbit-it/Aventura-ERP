# Generated by Django 3.1.14 on 2022-07-23 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_suivicommande_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandedAchat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fournisseur', models.CharField(max_length=64)),
                ('numero_bc', models.CharField(max_length=64)),
                ('numero_facture', models.CharField(default='', max_length=64)),
                ('etat_paiement', models.CharField(default='', max_length=64)),
                ('is_confirmed', models.BooleanField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='suivicommande',
            old_name='date',
            new_name='date_position',
        ),
        migrations.RemoveField(
            model_name='suivicommande',
            name='arriver_chez_gts',
        ),
        migrations.RemoveField(
            model_name='suivicommande',
            name='chez_fournisseur',
        ),
        migrations.RemoveField(
            model_name='suivicommande',
            name='en_transit',
        ),
        migrations.RemoveField(
            model_name='suivicommande',
            name='etat_commande',
        ),
        migrations.RemoveField(
            model_name='suivicommande',
            name='livraison_stgi',
        ),
        migrations.RemoveField(
            model_name='suivicommande',
            name='livrer_fournisseur',
        ),
        migrations.AddField(
            model_name='suivicommande',
            name='suivi_position',
            field=models.CharField(default='', max_length=64),
        ),
    ]
