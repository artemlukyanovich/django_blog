# Generated by Django 3.0.7 on 2020-07-04 15:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0026_auto_20200704_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 7, 4, 18, 33, 16, 270624), null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 7, 4, 18, 33, 16, 271052), null=True),
        ),
    ]