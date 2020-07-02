# Generated by Django 2.2.14 on 2020-07-02 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyprice',
            name='close_value',
            field=models.FloatField(default=0.0, verbose_name='close'),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='high_value',
            field=models.FloatField(default=0.0, verbose_name='high'),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='low_value',
            field=models.FloatField(default=0.0, verbose_name='low'),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='open_value',
            field=models.FloatField(default=0.0, verbose_name='open'),
        ),
        migrations.AlterField(
            model_name='dailyprice',
            name='volume',
            field=models.IntegerField(default=0, verbose_name='volume'),
        ),
        migrations.AlterUniqueTogether(
            name='dailyprice',
            unique_together=set(),
        ),
    ]
