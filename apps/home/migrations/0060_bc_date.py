# Generated by Django 3.2.11 on 2022-10-06 00:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0059_bc_num_bc'),
    ]

    operations = [
        migrations.AddField(
            model_name='bc',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]