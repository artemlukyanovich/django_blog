# Generated by Django 3.0.7 on 2020-08-19 18:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0036_auto_20200819_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 21, 25, 27, 472074)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 21, 25, 27, 472548)),
        ),
    ]