# Generated by Django 3.0.7 on 2020-08-19 23:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0044_auto_20200820_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='SomeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 2, 30, 14, 852501)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 2, 30, 14, 853020)),
        ),
    ]
