#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import os
from pymongo import MongoClient
import config
import json
from ferdl import ferdl_out
import time

client = MongoClient('<mongoserver>')
db = client.collection

affected_users_checked = False


def batch(batch_cursor, n=1000):
    iterable = [item for item in batch_cursor]
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def save_to_file(cursor, language, link, body, device_name):
    i = 0
    total_devices = 0
    for chunk in batch(cursor):
        i += 1
        with open('{}_payload/{}_{}_{}'.format(config.current_folder_prefix, language, device_name, i), 'w') as jsonfile:
            dick = {
                "message": {
                    "title": '<title>',
                    "body": body,
                    "icon": "<logo>",
                },
                "data": {"link": link},
                "options": {
                    "sound": "default"
                },
                "devices": chunk
            }
            print('saving `{}` tokens in `{}` for `{}` with body `{}`'.format(
                str(len(chunk)), str(lang), str(device), str(body))
            )
            json.dump(dick, jsonfile)
            total_devices += len(chunk)
    return total_devices


def query(langs, device_name, block_check):
    print('counting affected users...')

    agg_query = {
        'push_subscriptions.n_type': 'message_center',
        'push_enabled': True,
        'push_devices.token': {'$exists': True},
    }

    if config.polygon:
        if not config.ref_field:
            raise ValueError('need ref_field to match the location for the polygon.')
        agg_query.update({
            config.ref_field: {
                '$geoWithin': {
                    '$geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': config.polygon,
                     }
                 }
            }
        })

    if config.criteria:
        agg_query.update(config.criteria)

    if not block_check:
        affected_countries = db.user.aggregate([
            {'$match': agg_query},
            {'$group': {
                '_id': '$country',
                'n': {'$sum': 1}
            }},
            {'$sort': {'n': -1}}
        ])

        print('users in following countries are covered by this area:')
        total_sum = 0
        countries = []
        for ctr in affected_countries:
            countries.append(ctr)
            total_sum += ctr['n']

        if total_sum == len(config.co_receiver):
            exit("message would only be sent to co-receivers, exiting...")

        print('total: ' + str(total_sum))
        print(str(countries).replace('}, {', '}\n{'))  # pretty bitch

    # add currently parsed langauge to query
    agg_query.update({'language': {'$in': langs}})

    query_cond = [
        {"display_name": {'$in': config.co_receiver}},
    ]

    if not config.co_receiver_only:
        query_cond.append(agg_query)

    print('query for `{}` in `{}`.'.format(str(device_name), str(lang)))
    cursor = db.user.aggregate([
        {'$match': {'$or': query_cond}},
        {'$unwind': '$push_devices'},
        {'$match': {'push_devices.platform': device_name}},
        {'$project': {device_name: '$push_devices.token', '_id': 0}},
    ])

    return cursor

os.mkdir('{}_payload'.format(config.current_folder_prefix))
total_devices = 0
for lang, data in config.languages.iteritems():
    for device in config.DEVICES:
        total_devices += save_to_file(
            cursor=query(data['match'], device, affected_users_checked),
            language=lang,
            link=data.get('link', config.DEEP_LINK),
            body=data['long_text'] if config.LONG_TEXT else data['short_text'],
            device_name=device
        )
        affected_users_checked = True

# doo iiiit
print("sending out {} notifications, start in {} seconds. interrupt if you dont have the balls to do it.".format(
    str(total_devices), "10"
))
time.sleep(10)
ferdl_out(config.current_folder_prefix, config.max_push_per_sec)
