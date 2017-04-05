# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from notifications.push.models import PushNotification, DeepLink, CoReceiver, Text, Language, Country


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

admin.site.register(Country)
admin.site.register(Language)
admin.site.register(CoReceiver)
admin.site.register(PushNotification, PushNotificationAdmin)
admin.site.register(DeepLink)
