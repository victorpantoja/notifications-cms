# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-05 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0004_auto_20170405_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_text', models.CharField(max_length=200)),
                ('short', models.CharField(max_length=200)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='push.Language')),
            ],
        ),
        migrations.AlterField(
            model_name='pushnotification',
            name='co_receivers',
            field=models.ManyToManyField(to='push.CoReceiver'),
        ),
        migrations.AddField(
            model_name='text',
            name='push',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='push.PushNotification'),
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='texts',
            field=models.ManyToManyField(through='push.Text', to='push.Language'),
        ),
    ]
