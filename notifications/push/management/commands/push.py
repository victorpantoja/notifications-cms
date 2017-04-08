# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from notifications.push.models import PushNotification


class Command(BaseCommand):
    help = 'Send push notifications'

    def add_arguments(self, parser):
        parser.add_argument('push_id', type=int)

    def handle(self, *args, **options):
        push_id = options['push_id']
        try:
            push = PushNotification.objects.get(pk=push_id)
        except PushNotification.DoesNotExist:
            raise CommandError('PushNotification "%s" does not exist' % push_id)

        # self.stdout.write(
        #     self.style.SUCCESS('Successfully send push notification "%s"' % push_id))
