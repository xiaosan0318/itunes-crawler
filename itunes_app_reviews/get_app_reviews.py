#!/usr/bin/env python
# encoding: utf-8

"""
Returns a list of reviews for the given App ID and AppStore ID.
The format of the list: [{"title": string, "stars": string, etc.}]

Source: https://github.com/grych/AppStoreReviews
"""

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import calendar
import datetime
import hashlib
import re
import time

from bs4 import BeautifulSoup
from itunes_utilities.get_appstore_id import get_appstore_id
from itunes_utilities.get_itunes_page import get_itunes_page


def get_app_reviews(appId, countryName):
    countryName = str(countryName).lower().title().strip()
    reviews     = list()
    pageNo      = 0
    maxPages    = 800
    while True:
        ret = _getReviewsForPage(appId, countryName, pageNo)
        if len(ret)==0 or pageNo>maxPages:
            break
        # end of if statement.
        reviews += ret  # Collate the reviews of every page. It's a list of Dictionary objects.
        pageNo  += 1    # Increment the page number.
        #print 'Finished page #%d (total reviews: %d)' % (pageNo, len(reviews))
    # End of while loop.
    return reviews
# End of get_app_reviews(...).


def get_dateFormat_of_countryName(countryName):
    dateFormat = {
        'Australia'         : '%b %d, %Y',
        'Canada'            : '%b %d, %Y',
        'Singapore'         : '%b %d, %Y',
        'United Kingdom'    : '%b %d, %Y',
        'United States'     : '%b %d, %Y'
    } # End of dateFormat.
    output = dateFormat.get(countryName)
    if output is None:  # If the country is not listed...
        output = '%b %d, %Y' # ... use the default.
    # End of if statement.
    return output
# End of get_countryName_dateFormat(...).


def _getReviewsForPage(appId, countryName, pageNo):
    url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=%d&sortOrdering=4&onlyLatestVersion=false&type=Purple+Software" % (appId, pageNo)
    ret = list() # The list to be returned.
    try:
        appStoreId  = int(get_appstore_id(countryName)) # Note that this may return a None.
        soup        = BeautifulSoup(get_itunes_page(url, appStoreId))
        reviews     = soup.findAll('hboxview', attrs = {'bottominset':'3'})
        for i in range(0, len(reviews)):
            try:
                review = reviews[i]
                #========================#
                # Retrieve: title, stars #
                #========================#
                temp_var_1  = review.find('textview')
                title       = temp_var_1.text.strip()
                temp_stars  = temp_var_1.findNext('hboxview', attrs = {'topinset':'1'})['alt'].strip()
                find_stars  = re.compile(r'\d')
                stars       = re.search(find_stars, temp_stars).group()
                #==================================================#
                # Retrieve: user, user_url, user_id, version, date #
                #==================================================#
                temp_var_2 = temp_var_1.findNext('textview', attrs = {'topinset':'0', 'truncation':'right', 'leftinset':'0', 'squishiness':'1', 'styleset':'basic13', 'textjust':'left', 'maxlines':'1'})
                user = temp_var_2.find('b')
                #============================#
                # Check if the user is None. #
                #============================#
                if user is None :
                    print "Skipping this user coz user is None."
                    continue
                else:
                    user = user.text.strip()
                    if user.lower() == 'anonymous':
                        print "Skipping this user coz user is Anonymous."
                        continue
                    else:
                        try:
                            user_url        = str(temp_var_2.find('gotourl')['url'].strip())
                            find_user_id    = re.compile(r'\d+')                                        # Alternative: find_user_id = re.compile(r'^.+userProfileId=')
                            user_id         = str(re.search(find_user_id, user_url).group().strip())    # Alternative: user_id = filter(None, re.split(find_user_id, user_url))[0]
                        except Exception, e:
                            print "Skipping this user coz user is Unknown (exception msg: %s)." % e
                            continue
                        # End of try/except statement.
                    # End of if/else statement.
                    version                 = ''
                    formattedDate           = None
                    formattedDateUnixTime   = 0
                    try:
                        temp_list = re.compile(r'\s-\s').split(temp_var_2.text)
                        temp_list_index = 0
                        for j in temp_list:
                            if re.search(r'(Version)', j):
                                version                 = j.lower().replace('version', '').strip()
                                date                    = temp_list[temp_list_index+1].strip()
                                formattedDate           = datetime.datetime.strptime(date, get_dateFormat_of_countryName(countryName))
                                formattedDateUnixTime   = calendar.timegm(formattedDate.timetuple())
                            # End of if statement.
                            temp_list_index += 1
                        # End of for loop.
                    except Exception, e:
                        print "Skipping this user coz unable to determine the date of the review (exception msg: %s)." % e
                        continue
                    # End of try/except statement.
                # End of if/else statement.
                #=======================#
                # Retrieve: description #
                #=======================#
                temp_var_3  = temp_var_2.findNext('textview')
                description = temp_var_3.text.strip()
                #========================================#
                # Store the information in a Dictionary. #
                #========================================#
                try:
                    d                       = dict()
                    d['_id']                = str(appId) + '_' + str(user_id)
                    d['_id']                = hashlib.md5(d['_id']).hexdigest() # Remember: import hashlib
                    d['trackId']            = int(appId)
                    d['title']              = unicode(title).encode('utf-8')
                    d['rating']             = int(stars)
                    d['userName']           = unicode(user).encode('utf-8')
                    d['userViewUrl']        = unicode(user_url).encode('utf-8')
                    d['userId']             = int(user_id)
                    d['version']            = unicode(version).encode('utf-8')
                    d['date']               = formattedDate.strftime('%Y-%m-%d %H:%M:%S')
                    d['dateUnixTime']       = formattedDateUnixTime
                    d['description']        = unicode(description).encode('utf-8')
                    d['countryName']        = countryName
                    d['appStoreId']         = appStoreId
                    d['crawledUnixTime']    = int(time.time())
                    d['crawledTime']        = datetime.datetime.fromtimestamp(d['crawledUnixTime']).strftime('%Y-%m-%d %H:%M:%S')
                    ret.append(d)
                except Exception, e:
                    print "Skipping this user coz unable to store info into a Dictionary (exception msg: %s)." % e
                    continue
                # End of try/except statement.
            except Exception, e:
                print 'Skipping this review coz an exception occured (exception msg: %s).' % e
                continue
            # End of try/except statement.
        # End of for loop.
    except Exception, e:
        print 'An exception has occured in "_getReviewsForPage(...)": %s' % e
        pass
    # End of try/except statement.
    return ret
# End of _getReviewsForPage(...).


def main():
    print '\nStart!\n'

    countryName = 'SingaPOre  '
    reviews = get_app_reviews(511999255, countryName) # Burpple
    #reviews = get_app_reviews(557137623, countryName) # Angry Birds Star Wars

    print 'No. of reviews (%s): %i\n' % (countryName, len(reviews))

    for index, myDictionary in enumerate(reviews):
        print '#%s' % (index+1)
        list_of_sorted_keys = ['_id', 'trackId', 'title', 'rating', 'userName', 'userViewUrl', 'userId', 'version', 'date', 'dateUnixTime', 'description', 'countryName', 'appStoreId', 'crawledUnixTime', 'crawledTime']
        for key in list_of_sorted_keys:
            print '[%s] %s (%s)' % (key, myDictionary[key], type(myDictionary[key]))
        # End of for loop.
        print ''
    # End of for loop.

    print 'End!\n'
# End of main().

if __name__ == '__main__':
    main()