# Generated by Django 3.1.14 on 2022-07-11 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20220710_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='pu_demande',
            field=models.FloatField(default=0),
        ),
    ]
