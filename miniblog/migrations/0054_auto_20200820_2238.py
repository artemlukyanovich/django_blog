# Generated by Django 3.0.7 on 2020-08-20 19:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0053_auto_20200820_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='mod_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 22, 38, 14, 997481)),
        ),
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 22, 38, 14, 997455), editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 22, 38, 14, 997977)),
        ),
    ]
