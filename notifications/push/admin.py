# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from notifications.push.models import PushNotification, DeepLink, CoReceiver, Text, Language, Country, \
    Polygon


class TextInline(admin.TabularInline):
    model = Text


class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ('description', 'date')
    inlines = (TextInline,)
    fieldsets = [
        (None, {'fields': ['description', 'date']}),
        ("Filters", {'fields': ['countries', 'last_login']}),
        ('Co Receivers', {'fields': ['co_receivers_only', 'co_receivers']}),
        (None, {'fields': ['ready']}),
        ('Message', {'fields': ['deep_link']}),
    ]


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'matches')


admin.site.register(Country)
admin.site.register(Language, LanguageAdmin)
admin.site.register(CoReceiver)
admin.site.register(PushNotification, PushNotificationAdmin)
admin.site.register(DeepLink)
admin.site.register(Polygon, LeafletGeoAdmin)
