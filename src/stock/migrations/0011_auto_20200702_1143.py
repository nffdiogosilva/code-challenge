# Generated by Django 2.2.13 on 2020-07-02 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_auto_20200702_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyprice',
            name='created_at',
            field=models.DateField(verbose_name='created_at'),
        ),
    ]
