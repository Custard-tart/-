# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0016_auto_20180925_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
