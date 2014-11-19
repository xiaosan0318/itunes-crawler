#!/usr/bin/env python
# encoding: utf-8

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import datetime
import json
import time

from itunes_app_info.get_app_json import get_app_json
from itunes_app_info.get_app_updated_date import get_app_updated_date


def get_app_info(app_id):
    json_data = get_app_json(app_id)
    if json_data:
        try:
            result = json.loads(json_data)['results'][0] # Result is a Dictionary type.
            #===================#
            # App info (basic). #
            #===================#
            trackId                 = int(result['trackId'])                        # int
            trackName               = result['trackName'].encode('utf-8')           # Take note of unicode to utf-8
            trackViewUrl            = result['trackViewUrl'].encode('utf-8')        # Take note of unicode to utf-8
            trackContentRating      = result['trackContentRating'].encode('utf-8')  # Take note of unicode to utf-8
            trackCensoredName       = result['trackCensoredName'].encode('utf-8')   # Take note of unicode to utf-8
            try:    description     = result['description'].encode('utf-8')         # Take note of unicode to utf-8
            except: description     = ''
            try:    releaseNotes    = result['releaseNotes'].encode('utf-8')        # Take note of unicode to utf-8
            except: releaseNotes    = ''
            price                   = float(result['price'])                        # float
            formattedPrice          = result['formattedPrice'].encode('utf-8')      # Take note of unicode to utf-8
            currency                = result['currency'].encode('utf-8')            # Take note of unicode to utf-8
            #================================#
            # Release Date and Updated Date. #
            #================================#
            releaseDate     = (datetime.datetime.strptime(result['releaseDate'], '%Y-%m-%dT%H:%M:%SZ')).strftime('%Y-%m-%d %H:%M:%S')
            updatedDateDict = get_app_updated_date(app_id)
            if updatedDateDict is not None:
                updatedDate = updatedDateDict['datetime']
            else:
                updatedDate = ''
            #===========================#
            # App info (miscellaneous). #
            #===========================#
            version                 = result['version'].encode('utf-8')                         # Take note of unicode to utf-8
            fileSizeBytes           = int(result['fileSizeBytes'])                              # int
            bundleId                = result['bundleId'].encode('utf-8')                        # Take note of unicode to utf-8
            languageCodesISO2A      = ','.join(result['languageCodesISO2A']).encode('utf-8')    # Take note of unicode to utf-8
            supportedDevices        = ','.join(result['supportedDevices']).encode('utf-8')      # Take note of unicode to utf-8
            features                = ','.join(result['features']).encode('utf-8')              # Take note of unicode to utf-8
            contentAdvisoryRating   = result['contentAdvisoryRating'].encode('utf-8')           # Take note of unicode to utf-8
            isGameCenterEnabled     = result['isGameCenterEnabled']                             # boolean
            kind                    = result['kind'].encode('utf-8')                            # Take note of unicode to utf-8
            wrapperType             = result['wrapperType'].encode('utf-8')                     # Take note of unicode to utf-8
            #===========#
            # Category. #
            #===========#
            genreIds            = ','.join(result['genreIds']).encode('utf-8')  # Take note of unicode to utf-8
            genres              = ','.join(result['genres']).encode('utf-8')    # Take note of unicode to utf-8
            primaryGenreId      = int(result['primaryGenreId'])                 # int
            primaryGenreName    = result['primaryGenreName'].encode('utf-8')    # Take note of unicode to utf-8
            #==========#
            # Ratings. #
            #==========#
            try:
                averageUserRatingForCurrentVersion  = int(result['averageUserRatingForCurrentVersion'])
                userRatingCountForCurrentVersion    = int(result['userRatingCountForCurrentVersion'])
            except:
                averageUserRatingForCurrentVersion  = 0
                userRatingCountForCurrentVersion    = 0
            try:
                averageUserRating   = int(result['averageUserRating'])
                userRatingCount     = int(result['userRatingCount'])
            except:
                averageUserRating   = 0
                userRatingCount     = 0
            #======================#
            # About the developer. #
            #======================#
            artistId            = int(result['artistId'])                   # int
            artistName          = result['artistName'].encode('utf-8')      # Take note of unicode to utf-8
            artistViewUrl       = result['artistViewUrl'].encode('utf-8')   # Take note of unicode to utf-8
            sellerName          = result['sellerName'].encode('utf-8')      # Take note of unicode to utf-8
            try:    sellerUrl   = result['sellerUrl'].encode('utf-8')       # Take note of unicode to utf-8
            except: sellerUrl   = ''
            #=============================#
            # Artworks, screenshots, etc. #
            #=============================#
            artworkUrl60        = result['artworkUrl60'].encode('utf-8')                    # Take note of unicode to utf-8
            artworkUrl100       = result['artworkUrl100'].encode('utf-8')                   # Take note of unicode to utf-8
            artworkUrl512       = result['artworkUrl512'].encode('utf-8')                   # Take note of unicode to utf-8
            screenshotUrls      = ','.join(result['screenshotUrls']).encode('utf-8')        # Take note of unicode to utf-8
            ipadScreenshotUrls  = ','.join(result['ipadScreenshotUrls']).encode('utf-8')    # Take note of unicode to utf-8
            #======================#
            # Store in dictionary. #
            #======================#
            d = dict()
            d['trackId']                            = trackId
            d['trackName']                          = trackName
            d['trackViewUrl']                       = trackViewUrl
            d['trackContentRating']                 = trackContentRating
            d['trackCensoredName']                  = trackCensoredName
            d['description']                        = description
            d['releaseNotes']                       = releaseNotes
            d['price']                              = price
            d['formattedPrice']                     = formattedPrice
            d['currency']                           = currency
            d['releaseDate']                        = releaseDate
            d['updatedDate']                        = updatedDate
            d['version']                            = version
            d['fileSizeBytes']                      = fileSizeBytes
            d['bundleId']                           = bundleId
            d['languageCodesISO2A']                 = languageCodesISO2A
            d['supportedDevices']                   = supportedDevices
            d['features']                           = features
            d['contentAdvisoryRating']              = contentAdvisoryRating
            d['isGameCenterEnabled']                = isGameCenterEnabled
            d['kind']                               = kind
            d['wrapperType']                        = wrapperType
            d['genreIds']                           = genreIds
            d['genres']                             = genres
            d['primaryGenreId']                     = primaryGenreId
            d['primaryGenreName']                   = primaryGenreName
            d['averageUserRatingForCurrentVersion'] = averageUserRatingForCurrentVersion
            d['userRatingCountForCurrentVersion']   = userRatingCountForCurrentVersion
            d['averageUserRating']                  = averageUserRating
            d['userRatingCount']                    = userRatingCount
            d['artistId']                           = artistId
            d['artistName']                         = artistName
            d['artistViewUrl']                      = artistViewUrl
            d['sellerName']                         = sellerName
            d['sellerUrl']                          = sellerUrl
            d['artworkUrl60']                       = artworkUrl60
            d['artworkUrl100']                      = artworkUrl100
            d['artworkUrl512']                      = artworkUrl512
            d['screenshotUrls']                     = screenshotUrls
            d['ipadScreenshotUrls']                 = ipadScreenshotUrls
            d['crawledUnixTime']                    = int(time.time())
            d['crawledTime']                        = datetime.datetime.fromtimestamp(d['crawledUnixTime']).strftime('%Y-%m-%d %H:%M:%S')
            return d
        except Exception, e:
            print e
            return None
        # End of try/except statement.
    else:
        return None
    # End of if/else statement.
# End of get_app_info(...).


def main():
    d = get_app_info(511999255) # Burpple
    #d = get_app_info(557137623) # Angry Birds Star Wars
    if d:
        for k in d:
            print '[%s] %s (%s)' % (k, d[k], type(d[k]))
        # End of for loop.
    # End of if statement.
    else:
        print 'Nothing...'
    # End of else statement.
# End of main().

if __name__ == "__main__":
    main()