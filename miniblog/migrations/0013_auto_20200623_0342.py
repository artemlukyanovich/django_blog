# Generated by Django 3.0.7 on 2020-06-23 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0012_auto_20200622_0126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
