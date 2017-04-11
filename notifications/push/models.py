# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djgeojson.fields import GeoJSONField


class Base(object):
    def as_json(self):
        opts = self._meta
        data = {}
        for field in opts.concrete_fields + opts.many_to_many:
            if isinstance(field, models.ManyToManyField):
                data[field.name] = [obj.as_json() for obj in getattr(self, field.name).all()]
            elif isinstance(field, models.ForeignKey):
                data[field.name] = getattr(self, field.name).as_json()
            else:
                data[field.name] = field.value_from_object(self)
        return data


class Polygon(models.Model, Base):
    description = models.CharField(max_length=200)
    geom = GeoJSONField("Geometry")

    def __str__(self):
        return self.description


class MessageConfig(models.Model, Base):
    title = models.CharField(max_length=20)
    icon = models.CharField(max_length=20)

    def __str__(self):
        return "Title: {}. Icon: {}".format(self.title, self.icon)


class CoReceiver(models.Model, Base):
    display_name = models.CharField("Display Name", max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.display_name


class DeepLink(models.Model, Base):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model, Base):
    iso_code = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    matches = models.CharField(max_length=20,
                               help_text="Comma-separated values of languages "
                                         "to match")

    def __str__(self):
        return "{} ({})".format(self.name, self.iso_code)


class Country(models.Model, Base):
    iso_code = models.CharField(max_length=2)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return "{} ({})".format(self.name, self.iso_code)


# class ABTest(models.Model):
#
#     groups =

class PushNotification(models.Model, Base):
    description = models.CharField(max_length=200)
    date = models.DateTimeField('Push Date',
                                help_text="Date that this push notification "
                                          "must be sent")

    message_config = models.ForeignKey(MessageConfig,
                                       help_text="Defines message's title and icon")

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


class Text(models.Model, Base):
    long_text = models.CharField(max_length=200)
    short = models.CharField(max_length=200)
    push = models.ForeignKey(PushNotification)
    language = models.ForeignKey(Language)


class Result(models.Model, Base):
    push = models.ForeignKey(PushNotification)
    success = models.IntegerField()
    fail = models.IntegerField()
