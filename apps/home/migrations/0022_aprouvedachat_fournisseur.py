# Generated by Django 3.1.14 on 2022-07-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20220718_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='aprouvedachat',
            name='fournisseur',
            field=models.CharField(default='', max_length=64),
        ),
    ]
