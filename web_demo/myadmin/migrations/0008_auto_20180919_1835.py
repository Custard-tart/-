# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0007_auto_20180919_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartgoods',
            name='num',
            field=models.IntegerField(),
        ),
    ]
