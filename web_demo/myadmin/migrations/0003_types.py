# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-15 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_auto_20180912_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('pid', models.IntegerField()),
                ('path', models.CharField(max_length=50)),
                ('pname', models.CharField(max_length=20)),
            ],
        ),
    ]
