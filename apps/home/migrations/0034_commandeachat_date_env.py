# Generated by Django 3.1.14 on 2022-07-31 11:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20220731_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandeachat',
            name='date_env',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
