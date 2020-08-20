# Generated by Django 3.0.7 on 2020-08-19 18:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0037_auto_20200819_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='autodescription',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 21, 27, 7, 496792)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 21, 27, 7, 497318)),
        ),
    ]