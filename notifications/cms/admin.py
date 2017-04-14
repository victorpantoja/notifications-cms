# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from notifications.cms.models import ManageAlerts

admin.site.register(ManageAlerts)
