# -*- coding: utf-8 -*-
import datetime
import os

import pytz
import ujson

from pytz import country_timezones
from ref import known_contries_in_db
import time

disabled = False


def where_is_it_time_to_send(current_utc_time, shall_send_at, verbose=True):
    time_we_need = "not detected"
    matching_countries = []
    for country in known_contries_in_db:
        timezone_there = country_timezones(country.lower())[0]
        country_timezones(country.lower())
        time_there = current_utc_time.astimezone(pytz.timezone(timezone_there))
        time_obj_there = datetime.datetime(
            time_there.year, time_there.month, time_there.day, time_there.hour
        )

        if (time_obj_there - shall_send_at).total_seconds() == 0:
            time_we_need = time_there
            matching_countries.append(country)

    if matching_countries and verbose:
        print('currently its {utc} utc and we need to send in {ctr} because its {local} there'.format(
            utc=str(current_utc_time), ctr=",".join(matching_countries), local=str(time_we_need)
        ))

    return matching_countries

# display name of all co-receivers (just for checking encoding and sltuffness)
co_receiver = [

]
# for testing / formatting etc...
co_receiver_only = False

max_push_per_sec = 400
# hans, schaut wie spaet es ist
hansguckaufdieuhr = datetime.datetime.now(tz=pytz.UTC)

# when do we want to deliver in user's local time.
user_receive_time_utc = datetime.datetime(2017, 3, 31, 17)

current_folder_prefix = timestamp = int(time.time())

# will be converted tso user timezone
countries_matched = []
countries_collided = []
# test for collisions
for h in range(-24 * 5, 24 * 5):
    _user_receive_time_utc = user_receive_time_utc + datetime.timedelta(hours=h)
    send_countries = where_is_it_time_to_send(hansguckaufdieuhr, _user_receive_time_utc, False)
    if send_countries:
        for matched_country in send_countries:
            if matched_country in countries_matched:
                countries_collided.append(matched_country)
            else:
                countries_matched.append(matched_country)

# self check of correct timezone handling
# assert len(countries_collided) == 0
# assert len(countries_matched) == len(known_contries_in_db)

# ref_field of coordinates (recent location, any of his locations, ...)
ref_field = 'recent_location.coordinates'

# polygon restriction in case of a file with a polygon was found.
try:
    with open('polygon.json', 'r') as polyfile:
        print("using polygon!")
        content_strin = polyfile.read().strip('\n ')
        polygon = ujson.loads(content_strin)
except IOError as ex:
    print("ignoring polygon, {}".format(str(ex)))
    polygon = None


# additional criteria to match users
#countries_to_send_now = where_is_it_time_to_send(hansguckaufdieuhr, user_receive_time_utc)

#if not countries_to_send_now:
#     print('nothing to be sent at {} utc. next job at {} in each user time zone.'.format(str(hansguckaufdieuhr), str(user_receive_time_utc)))
#     exit()

# exclude_ids_obj = []
# with open('user_query.json', 'rb') as f:
#     exclude_ids_str = list(csv.reader(f))[0]
#     for _id in exclude_ids_str:
#         exclude_ids_obj.append(ObjectId(_id))
#     print("excluding {} users from exclude file".format(len(exclude_ids_obj)))

# use it as a base for all countries and remove and you needn't
# limit_countries = ['AT', 'DE', 'ES', 'FR', 'HR', 'RS', 'CZ'
#                    'IT', 'PT', 'HU', 'RO', 'SK', 'NL', 'PL']
limit_countries = ['HR', 'RS', 'IT', 'PT', 'HU', 'RO', 'SK', 'CZ', 'PL', 'NL']

LONG_TEXT = int(os.getenv("LONG_TEXT", 1)) == 1

print("{}using long texts".format("" if LONG_TEXT else "not "))

groups = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] \
    if LONG_TEXT else [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

criteria = {
    #"last_login": {"$lt": datetime.datetime.now() - datetime.timedelta(days=14), "$gt": datetime.datetime.now() - datetime.timedelta(days=90)},
    #"country": {"$in": countries_to_send_now},
    "recent_country": {"$in": limit_countries},
    #"group": {"$in": groups},
    #"language": {"$in": ["de", "de-ch", "de-de", "de-at"]},
    #"_id": {"$nin": exclude_ids_obj}
}

DEVICES = ['fcm', 'gcm', 'apns']
DEEP_LINK = '<deep link>'

# language / text config. only users of those languages will match.
languages = {
    # 'en': {
    #     'match': ["en", "en-au", "en-gb", "en-us"],
    #     'long_text': "",
    #     'short_text': ''
    # },
    # 'de': {
    #     'match': ["de", "de-ch", "de-de", "de-at"],
    #     'long_text': "",
    #     'short_text': ''
    # },
    # 'es': {
    #     'match': ["es", "es_CL", "es_CO", "es_LA", "es_MX"],
    #     'long_text': "",
    #     'short_text': ''
    # },
    # 'fr': {
    #     'match': ["fr", "fr_CA"],
    #     'long_text': "",
    #     'short_text': ''
    # },
}

if disabled:
    exit('I am on vacation.')
