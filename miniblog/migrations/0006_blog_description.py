# Generated by Django 3.0.7 on 2020-06-17 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0005_auto_20200613_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.TextField(default='default_description', max_length=1000),
            preserve_default=False,
        ),
    ]
