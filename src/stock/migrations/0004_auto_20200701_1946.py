# Generated by Django 2.2.13 on 2020-07-01 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20200701_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='ticker',
            field=models.CharField(max_length=20, unique=True, verbose_name='Ticker'),
        ),
    ]