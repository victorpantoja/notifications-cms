# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-05 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0005_auto_20170405_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coreceiver',
            name='name',
            field=models.CharField(default='no name', max_length=20),
        ),
    ]