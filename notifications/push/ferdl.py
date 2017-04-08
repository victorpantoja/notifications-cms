# -*- coding: utf-8 -*-
import os
import requests
import json
import csv
import time


def send(payload):
    r = requests.post(
        '<push-server>',
        data=payload,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'text/plain; charset=utf-8'
        }
    )
    print('status from pushfred: ' + str(r.status_code))
    return r.json()


def get_result_key(result, key):
    for platform in ['apns', 'gcm', 'fcm']:
        successes = result.get(platform, None)
        if successes:
            try:
                return successes[key]
            except KeyError:
                return []


def ferdl_out(prefix, max_push_per_sec):
    prefix = str(prefix)
    results_dir = '{}_results'.format(prefix)
    os.mkdir(results_dir)

    with open(os.getcwd() + '/' + prefix + '_results/summary.json', 'w') as summary_file:
        with open(os.getcwd() + '/' + prefix + '_results/log.json', 'w') as log:
            with open(os.getcwd() + '/' + prefix + '_results/error_tokens.json', 'wb') as error_log:
                with open(os.getcwd() + '/' + prefix + '_results/cannonical_tokens.json', 'wb') as cannonical_log:
                    wr = csv.writer(error_log, quoting=csv.QUOTE_ALL)
                    wrc = csv.writer(cannonical_log, quoting=csv.QUOTE_ALL)
                    summary = {}
                    dirpath = os.getcwd() + '/' + prefix + '_payload/'
                    for filename in os.listdir(dirpath):
                        print('processing {}'.format(filename))
                        if filename.startswith('.') or filename.startswith('processed'):
                            continue

                        with open(os.getcwd() + '/' + prefix + '_payload/' + filename, 'r') as payload:
                            print('sending payload from `{}`'.format(str(filename)))

                            started_at = time.time()
                            try:
                                result = send(payload=payload)
                            except Exception as ex:
                                print(str(ex))
                                try:
                                    print("smth in {} fucked up but we are continuing.".format(str(prefix) + '/' + str(filename)))
                                except Exception:
                                    print(str(ex))
                                    pass
                                continue

                            send_time_dur = time.time() - started_at

                            res_dict = {
                                'payload_file': filename,
                                'result': result
                            }
                            json.dump(res_dict, log)
                            error_list = get_result_key(result['info'], 'failures')
                            try:
                                cannonical_list = get_result_key(result['info'], 'canonical_ids')
                                if cannonical_list:
                                    wrc.writerow(cannonical_list)
                            except Exception as ex:
                                print(ex.message)

                            n_errors = 0
                            if error_list:
                                n_errors = len(error_list)
                                wr.writerow(error_list)
                            summary.update({
                                filename: {
                                    'success': get_result_key(result['info'], 'successes'),
                                    'failures': n_errors,
                                    # todo all error tokens list here
                                }
                            })

                        os.rename(os.getcwd() + '/' + prefix + '_payload/' + filename, os.getcwd() + '/' + prefix + '_payload/' + 'processed_' + filename)

                        # autothrottle to not be a trottl
                        n_successes = get_result_key(result['info'], 'successes') or 0
                        waittime_suggested = n_successes / max_push_per_sec
                        waittime = waittime_suggested - send_time_dur if waittime_suggested - send_time_dur > 0 else 0
                        print("{} successful, {} failed, chilling for {} seconds, suggested:{} but sending took: {}".format(n_successes, n_errors, waittime, waittime_suggested, str(int(send_time_dur))))
                        time.sleep(waittime)
                    json.dump(summary, summary_file)
