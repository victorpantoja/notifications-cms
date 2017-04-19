# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from notifications.push.models import PushNotification, DeepLink, CoReceiver, Text, Language, Country, \
    Polygon, Result, MessageConfig


class TextInline(admin.TabularInline):
    model = Text


class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'ready',)
    inlines = (TextInline,)
    fieldsets = [
        (None, {'fields': ['description', 'date']}),
        ("Filters", {'fields': ['countries', 'last_login', 'polygon']}),
        ('Co Receivers', {'fields': ['co_receivers_only', 'co_receivers']}),
        (None, {'fields': ['ready']}),
        ('Message', {'fields': ['message_config', 'deep_link']}),
    ]

    search_fields = ['description']
    list_filter = ['date']

    save_as = True
    #
    # def save_model(self, request, obj, form, changed):
    #     if '_continue' in request.POST:
    #     # add your code here
    #     return super(ServerAdmin, self).change_view(request, obj, form, changed)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'matches')


class ResultAdmin(admin.ModelAdmin):
    readonly_fields = ('success', 'push', 'fail')


class MessageConfigAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')


admin.site.register(Country)
admin.site.register(Language, LanguageAdmin)
admin.site.register(CoReceiver)
admin.site.register(MessageConfig, MessageConfigAdmin)
admin.site.register(PushNotification, PushNotificationAdmin)
admin.site.register(DeepLink)
admin.site.register(Result, ResultAdmin)
admin.site.register(Polygon, LeafletGeoAdmin)
