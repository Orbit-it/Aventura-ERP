# Generated by Django 3.1.14 on 2022-07-31 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_remove_commandeachat_date_envoyee'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandeToSend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fournisseur', models.CharField(default='', max_length=64)),
                ('numero', models.CharField(default='', max_length=64)),
            ],
        ),
    ]