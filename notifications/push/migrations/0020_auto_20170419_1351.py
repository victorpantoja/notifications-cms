# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0019_pushnotification_polygon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushnotification',
            name='polygon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='push.Polygon'),
        ),
    ]
