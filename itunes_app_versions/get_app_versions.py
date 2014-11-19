#!/usr/bin/env python
# encoding: utf-8

"""
NOTE:
    APPANNIE.COM HAS IMPLEMENTED BOT-DETECTION.
    IN ORDER TO ASSURE A SMOOTH CRAWLING PROCESS, WE HAVE PLACED A
    COUPLE OF BOT-DETECTION MEASURES TO MAXIMIZE THE CRAWLING EFFICIENCY.

Description:
    Returns a list of "versions" for the given App ID.
    Each "version" is a Dictionary object.
    The format of the Dictionary is:
        [{"_id": string, "app_id": int, "date": string, "unixtime": int, "number": string, "updates": list}]
"""

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import calendar
import datetime
import hashlib
import re

from bs4 import BeautifulSoup
import spynner


#=======================#
# App Annie's statuses. #
#=======================#
STATUS_ERROR                 = 0
STATUS_OK                    = 1
STATUS_BOT_SPOTTED           = 2
STATUS_STILL_RETRIEVING_DATA = 3
STATUS_404_ERROR             = 4


def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)
# End of removeNonAscii(...).


def get_app_versions(app_id, spynner_browser_instance):
    app_id = int(app_id)
    url = 'http://www.appannie.com/app/ios/%s/' % app_id
    output_list = list()
    try:
        spynner_browser_instance.load(url, load_timeout=100, tries=3)
        html = spynner_browser_instance.html
        soup = BeautifulSoup(html)

        #======================================#
        # Check if App Annie detected our bot. #
        #======================================#
        try:
            intro_text = soup.find('div', {'class': 'intro'}).find('p').text
            intro_text = intro_text.lower()
            if 'Our systems have detected unusual traffic from your computer network'.lower() in intro_text:
                return STATUS_BOT_SPOTTED, None
            # End of if statement.
        except:
            pass
        # End of try/except statement.

        #===================================================#
        # Phew! App Annie still thinks that we are "human". #
        #===================================================#
        temp_list = soup.find('div', {'class': 'app-version-block'}).findAll('h5')
        for data in temp_list:
            line = unicode(data.text).strip().encode('utf-8')

            #==============================================#
            # Create Dictionary object and include App ID. #
            #==============================================#
            version = dict()
            version['app_id'] = app_id

            #===================================================#
            # Retrieve the "date" and "unixtime" of the update. #
            #===================================================#
            m = re.search(r'\((.+)\)', line)
            if m:
                try:
                    date = m.group(1)                                                # String
                    formatted_date = datetime.datetime.strptime(date, '%b %d, %Y')   # Datetime
                    formatted_unixtime = calendar.timegm(formatted_date.timetuple()) # Int
                except Exception, e:
                    print 'Exception while converting to unixtime: %s' % e
                    date = formatted_unixtime = None
                # End of try/except statement.
            else:
                date = formatted_unixtime = None
            # End of if/else statement.
            version['date'] = date
            version['unixtime'] = formatted_unixtime

            #============================================#
            # Retrieve the version number of the update. #
            #============================================#
            if date is not None:
                m = re.search(r'Version (.+) \(', line)
                ver_num = m.group(1)
            else:
                ver_num = line.replace('Version', '').strip()
            # End of if/else statement.
            version['number'] = ver_num

            #======================================#
            # Generate a unique "_id" for MongoDB. #
            #======================================#
            version['_id'] = str(app_id) + '_' + str(ver_num)
            version['_id'] = hashlib.md5(version['_id']).hexdigest() # Remember: import hashlib

            version['updates'] = list()
            try:
                list_of_updates = data.findNext('div', {'class': 'app-version-note'}).findAll('p')
                for update in list_of_updates:
                    contents = update.contents
                    for content in contents:
                        if content.string is not None:                             # If it is a legitimate text, not like '<br/>' or something...
                            temp_text = removeNonAscii(content)                    # Remove non-ascii characters.                           
                            temp_text = unicode(temp_text).strip().encode('utf-8') # Encode to 'utf-8'.
                            temp_text = temp_text.replace('\n', ' ')               # Remove the '\n' from text.
                            if temp_text[0] == '-' or temp_text[0] == '*':
                                temp_text = temp_text[1:]
                                temp_text = temp_text.strip()
                            # End of if statement.
                            if temp_text:                                          # If text is not empty...
                                version['updates'].append(temp_text)               # Append to list.
                            # End of if statement.
                        # End of if statement.
                    # End of for loop.
                # End of for loop.
                output_list.append(version)
            except Exception:
                continue
            # End of try/except statement.
        # End of for loop.
        return STATUS_OK, output_list
    except Exception, e:
        print 'Exception msg from get_app_versions(...): %s | url: %s' % (e, url)
        return STATUS_ERROR, None
    # End of try/except statement.      
# End of get_app_versions(...)


def main():
    try:
        br = spynner.Browser()
        status, list_of_versions = get_app_versions(557137623, b)   # Angry Birds Star Wars
        #status, list_of_versions = get_app_versions(284882215, br) # Facebook
        #status, list_of_versions = get_app_versions(310633997, br) # Whatsapp
        if list_of_versions:
            for version in list_of_versions:
                print '_id:',      version['_id']
                print 'App ID:',   version['app_id']
                print 'Date:',     version['date']
                print 'Unixtime:', version['unixtime']
                print 'Number:',   version['number']
                for update in version['updates']:
                    print '-', update
                print ''
            # End of for loop.
        # End of if statement.
    finally:
        br.close()
    # End of try/finally statement.
# End of main().

if __name__ == '__main__':
    main()