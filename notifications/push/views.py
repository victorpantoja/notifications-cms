# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.push.models import PushNotification


class PushNotificationView(APIView):

    def get(self, request, push_id):
        push = get_object_or_404(PushNotification, pk=push_id)

        return Response(push.as_json())
