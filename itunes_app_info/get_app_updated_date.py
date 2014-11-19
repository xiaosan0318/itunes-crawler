#!/usr/bin/env python
# encoding: utf-8

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import calendar
import datetime

from bs4 import BeautifulSoup
from itunes_utilities.get_itunes_page import get_itunes_page


def get_app_updated_date(app_id):
    try:
        url       = 'https://itunes.apple.com/us/app/id%s?mt=8' % app_id
        soup      = BeautifulSoup(get_itunes_page(url))
        side_info = soup.findAll('textview', attrs = {'topinset':'0', 'truncation':'right', 'leftinset':'0', \
                                                      'rightinset':'0', 'styleset':'basic11', 'bottominset':'0', \
                                                      'textjust':'left', 'maxlines':'1'})
        text_list = list()
        for info in side_info:
            text_list.append(info.text.strip().lower())
        # End of for loop.
        updated_date_in_String   = (filter(lambda x: 'updated' in x, text_list)[0]).replace('updated', '').strip()
        updated_date_in_Datetime = datetime.datetime.strptime(updated_date_in_String, '%b %d, %Y')
        output                   = dict()
        output['unixtime']       = int(calendar.timegm(updated_date_in_Datetime.timetuple()))
        output['datetime']       = updated_date_in_Datetime.strftime('%Y-%m-%d %H:%M:%S')
        return output
    except:
        return None
    # End of try/except statement.
# End of get_app_updated_date(...).


def main():
    my_date = get_app_updated_date(511999255) # Burpple
    #Rmy_date = get_app_updated_date(557137623) # Angry Birds Star Wars
    if my_date:
        print '\n', my_date, '\n'
        print 'Datetime: %s (%s)' % (my_date['datetime'], type(my_date['datetime']))
        print 'Unixtime: %s (%s)' % (my_date['unixtime'], type(my_date['unixtime']))
    else:
        print 'None!'
    # End of if/else statement.
# End of main().

if __name__ == '__main__':
    main()