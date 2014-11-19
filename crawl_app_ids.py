#!/usr/bin/env python
# encoding: utf-8

import datetime
import json
import time
import urllib

import pymongo

from config.config_mongodb import *
from itunes_rss_feed.static_data import *


def get_app_ids(country_code, feed_type, genre_id, limit):
    output_list = list()
    url         = 'https://itunes.apple.com/%s/rss/%s/limit=%s/genre=%s/json' % (country_code, feed_type, limit, genre_id)
    json_data   = urllib.urlopen(url).read()
    dict_data   = json.loads(json_data)
    try:
        entries = dict_data['feed']['entry']
    except:
        entries = None
    # End of try/except statement.
    if entries:
        for entry in entries:
            try:
                app_id = entry['id']['attributes']['im:id']
                output_list.append(app_id)
            except Exception, e:
                print 'Skipping this entry coz: %s' % e.message
                continue
            # End of try/except statement.
        # End of for loop.
        return output_list
    else:
        return None
    # End of if/else statement.
# End of get_app_ids(...).


def crawl_app_ids(nth_run = -1):
    #==============================#
    # Prepare the big_output_list. #
    #==============================#
    limit = 300
    for i in COUNTRY_ISOS:
        country_code = COUNTRY_ISOS[i]
        for j in FEED_TYPES:
            feed_type = FEED_TYPES[j]
            for k in GENRE_IDS:
                genre_id = GENRE_IDS[k]
                list_of_app_ids = get_app_ids(country_code, feed_type, genre_id, limit)
                if list_of_app_ids:
                    #=======================#
                    # Get the crawled time. #
                    #=======================#
                    unix_time            = time.time()
                    crawled_unixtime     = int(unix_time)
                    crawled_datetime_str = str(datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S'))
                    #======================================#
                    # Iterate through the list of app IDs. #
                    #======================================#
                    for app_id in list_of_app_ids:
                        app_id = int(app_id)
                        #=====================================#
                        # Prepare the dictionary data object. #
                        #=====================================#
                        d                     = dict()
                        d['_id']              = app_id
                        d['app_id']           = app_id
                        d['crawled_unixtime'] = crawled_unixtime
                        d['crawled_time']     = crawled_datetime_str
                        #=================#
                        # Store the data. #
                        #=================#
                        connection  = pymongo.Connection(MONGODB_LOCATION)
                        mongodb     = connection[MONGODB_DATABASE]
                        collection  = mongodb[MONGODB_APP_IDS_COLLECTION]
                        status      = collection.save(d)
                        print 'Run: %-3s  |  Country: %-2s  |  FeedType: %-14s  |  Genre: %-18s  |  Status: %s' % (nth_run, country_code, j, k, status)
                    # End of for loop.
                # End of if statement.
            # End of for loop.
        # End of for loop.
    # End of for loop.
# End of crawl_app_ids().


def main():
    count = 0
    while True:
        count += 1
        print '\nStarting run #%d\n' % count

        try:
            crawl_app_ids(nth_run=count)
        except Exception, e:
            print 'Exception msg: %s' % e
            print 'Sleeping now...'
            time.sleep(900)  # Sleep for 15 mins.
            print 'Woke up from sleep.'
        # End of try/except statement.

    # End of while loop.
# End of main().

if __name__ == "__main__":
    main()