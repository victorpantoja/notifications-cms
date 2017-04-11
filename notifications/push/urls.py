"""notifications URL Configuration"""
from django.conf.urls import url

from notifications.push.views import PushNotificationView

urlpatterns = [
    url(r'^(\d+)$', PushNotificationView.as_view(), name="get_push"),
]
