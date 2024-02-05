# Generated by Django 3.2.11 on 2022-09-15 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_commandeachat_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sortiedirecte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_intern', models.CharField(default='', max_length=64)),
                ('designation', models.CharField(default='', max_length=64)),
                ('quantity', models.FloatField(default=0)),
                ('unity', models.CharField(default='P', max_length=64)),
                ('motif', models.CharField(default='', max_length=300)),
            ],
        ),
    ]