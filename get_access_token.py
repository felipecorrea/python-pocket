#!/usr/bin/env python
#
# vim: sw=4 ts=4 st=4
#
#  Copyright 2014 Felipe Borges <felipe10borges@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib.request
import urllib.parse
import simplejson
import webbrowser

REQUEST_TOKEN_URL = "https://getpocket.com/v3/oauth/request"
AUTHORIZE_REQUEST_URL = "https://getpocket.com/auth/authorize"
AUTHORIZE_REQUEST_TOKEN = "https://getpocket.com/v3/oauth/authorize"

REDIRECT_URI = 'http://goo.gl/kGuI6g'

def get_access_token(consumer_key, redirect_uri = REDIRECT_URI):
    parameters = {
            'consumer_key' : consumer_key,
            'redirect_uri' : redirect_uri }
    headers = { 'X-Accept': 'application/json' }

    data = urllib.parse.urlencode(parameters)
    request = urllib.request.Request(REQUEST_TOKEN_URL, data.encode('ascii'), headers)

    try:
        resp = urllib.request.urlopen(request)
    except Exception as e:
        print('Invalid response from Pocket requesting request_token: %s' % e)
        return


    request_token = simplejson.loads(resp.read())['code']

    print("\nI will try to start a browser so you can authorize the request token\n")

    parameters = {
            'request_token' : request_token,
            'redirect_uri' : redirect_uri }

    webbrowser.open(AUTHORIZE_REQUEST_URL + '?' + urllib.parse.urlencode(parameters))
    go_ahead = input('Did you authorized? (Y/N)')

    if not go_ahead: return

    parameters = {
            'consumer_key' : consumer_key,
            'code' : request_token }

    data = urllib.parse.urlencode(parameters)
    request = urllib.request.Request(AUTHORIZE_REQUEST_TOKEN, data.encode('ascii'), headers)
    resp = urllib.request.urlopen(request)

    access_token = simplejson.loads(resp.read())

    print("Your Pocket Access Token: %s" %  access_token['access_token'])
    return access_token['access_token']

def main():
    consumer_key = input("Consumer key? ")

    get_access_token(consumer_key)

if __name__ == "__main__":
    main()
