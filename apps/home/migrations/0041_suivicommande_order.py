# Generated by Django 3.1.14 on 2022-08-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_commande_is_ready'),
    ]

    operations = [
        migrations.AddField(
            model_name='suivicommande',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
