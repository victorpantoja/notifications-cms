# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 11:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0018_auto_20170418_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushnotification',
            name='polygon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='push.Polygon'),
        ),
    ]
