# Generated by Django 3.2.11 on 2022-10-10 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0065_dimensionachat_is_recalled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimensionachat',
            name='is_recalled',
        ),
        migrations.AddField(
            model_name='bc',
            name='is_recalled',
            field=models.BooleanField(default=0),
        ),
    ]
