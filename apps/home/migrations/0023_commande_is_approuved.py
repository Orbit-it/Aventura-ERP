# Generated by Django 3.1.14 on 2022-07-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_aprouvedachat_fournisseur'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='is_approuved',
            field=models.BooleanField(default=0),
        ),
    ]