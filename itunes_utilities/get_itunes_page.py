#!/usr/bin/env python
# encoding: utf-8

"""
=====================================================
This function gets the page source of an iTunes page.
=====================================================
"""

import time
import urllib2


def get_itunes_page(url, app_store_id=143441, debug=False): # Default appStoreId is the US App Store.
    no_of_tries = 0
    max_tries   = 5
    delay       = 3
    while no_of_tries < max_tries:
        no_of_tries += 1
        try:
            front       = '%d-1' % app_store_id
            user_agent  = 'iTunes/10.2.1 (Macintosh; Intel Mac OS X 10.7) AppleWebKit/534.20.8'
            headers     = {'X-Apple-Store-Front': front, 'User-Agent': user_agent}
            request     = urllib2.Request(url, None, headers)
            response    = urllib2.urlopen(request, timeout=30)
            try:
                return response.read()
            finally:
                response.close()
        except:
            timeout = delay * no_of_tries
            if debug:
                print 'Unable to access "%s". Retrying in %d seconds.' % (url, timeout)
            # End of if statement.
            time.sleep(timeout)
    # End of while loop.
    return None
# End of get_itunes_page(...).


def main():
    print 'Start'
    print get_itunes_page('http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewUsersUserReviews?userProfileId=5696')
    print 'Done'
# End of main().

if __name__ == '__main__':
    main()