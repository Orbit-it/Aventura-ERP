# Generated by Django 3.2.11 on 2022-09-14 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0043_auto_20220913_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='is_refused',
            field=models.BooleanField(default=0),
        ),
    ]
