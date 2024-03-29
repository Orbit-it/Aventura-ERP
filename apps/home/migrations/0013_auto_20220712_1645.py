# Generated by Django 3.1.14 on 2022-07-12 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20220711_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='article',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='fournisseur',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='quantity',
        ),
        migrations.AddField(
            model_name='commande',
            name='article_commande',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='commande',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commande',
            name='fournisseur_commande',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='commande',
            name='identifier_commande',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='commande',
            name='prix_comande',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='commande',
            name='pu_commande',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='commande',
            name='quantity_commande',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='commande',
            name='unity_commande',
            field=models.CharField(default='PIECE', max_length=10),
        ),
        migrations.AddField(
            model_name='commande',
            name='user_commande',
            field=models.CharField(default='', max_length=64),
        ),
    ]
