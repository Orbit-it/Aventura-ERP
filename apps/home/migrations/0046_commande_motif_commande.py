# Generated by Django 3.2.11 on 2022-09-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_refusedachat'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='motif_commande',
            field=models.CharField(default='', max_length=300),
        ),
    ]
