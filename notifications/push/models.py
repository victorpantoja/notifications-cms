# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CoReceiver(models.Model):
    display_name = models.CharField("Display Name", max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.display_name


class DeepLink(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model):
    iso_code = models.CharField(max_length=2)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{} ({})".format(self.name, self.iso_code)


class Country(models.Model):
    iso_code = models.CharField(max_length=2)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{} ({})".format(self.name, self.iso_code)


class PushNotification(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateTimeField('Push Date',
                                help_text="Date that this push notification must be sent")
    deep_link = models.ForeignKey(DeepLink)
    co_receivers_only = models.BooleanField(
        "Only co-receivers?",
        help_text="Check if you want to send only for test users.",
        default=True)
    co_receivers = models.ManyToManyField(CoReceiver)

    countries = models.ManyToManyField(Country)
    last_login = models.DateTimeField('Last Login', null=True)

    texts = models.ManyToManyField(Language, through='Text')

    ready = models.BooleanField("Ready to Send?",
                                help_text="Click if push are ready to be sent.",
                                default=False)

    def __str__(self):
        return self.description


class Text(models.Model):
    long_text = models.CharField(max_length=200)
    short = models.CharField(max_length=200)
    push = models.ForeignKey(PushNotification)
    language = models.ForeignKey(Language)
