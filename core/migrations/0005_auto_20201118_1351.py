# Generated by Django 3.1.3 on 2020-11-18 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201118_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonnote',
            name='day',
            field=models.CharField(max_length=500),
        ),
    ]
