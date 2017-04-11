"""notifications URL Configuration"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^push/', include('notifications.push.urls')),
    url(r'^admin/', admin.site.urls),
]
