# Generated by Django 3.1.14 on 2022-07-11 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_dimensionachat_identifier_dim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='user_permission',
            field=models.CharField(default='', max_length=64),
        ),
    ]
