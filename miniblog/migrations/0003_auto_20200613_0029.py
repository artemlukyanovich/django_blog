# Generated by Django 3.0.7 on 2020-06-12 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0002_auto_20200613_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='bio',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
