# Generated by Django 3.1 on 2020-08-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test2api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='uid',
            field=models.CharField(max_length=100),
        ),
    ]
