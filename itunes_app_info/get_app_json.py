#!/usr/bin/env python
# encoding: utf-8

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import json

from itunes_utilities.get_web_page import get_web_page


def get_app_json(app_id):
    try:
        url = 'http://itunes.apple.com/lookup?id=' + str(app_id)
        json_data = get_web_page(url).strip()
        dict_data = json.loads(json_data)
        if (dict_data['resultCount']) == 0:
            return None
        else:
            return json_data
        # End of if/else statement.
    except:
        return None
    # End of try/except statement.
# End of get_app_json(...).


def main():
    json_data = get_app_json(557137623) # Angry Birds Star Wars
    if json_data is not None:
        print json_data
    else:
        print 'None!'
    # End of if/else statement.
# End of main().

if __name__ == "__main__":
    main()