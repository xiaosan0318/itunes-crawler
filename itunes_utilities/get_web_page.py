#!/usr/bin/env python
# encoding: utf-8

"""
=================================================
This function gets the page source of a Web page. 
=================================================
"""

import time
import urllib2


def get_web_page(url, debug=False):
    no_of_tries = 0
    max_tries   = 5
    delay       = 3
    while no_of_tries < max_tries:
        no_of_tries += 1
        try:
            user_agent  = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1'
            headers     = {'User-Agent' : user_agent}
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
# End of get_web_page(...).


def main():
    print 'Start'
    print get_web_page('http://jovianlin.com')
    print 'Done'
# End of main().

if __name__ == '__main__':
    main()