#!/usr/bin/env python2.7

# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

''' HTTP API extensions of COSC (versus ODL). 

    @author: Ken Jarrad (kjarrad@cisco.com)
'''

from __future__ import print_function as _print_function
from requests import post

def cosc_authentication_token(hostname='localhost', port=8181, username='admin', password='admin'):
    """ Obtain authentication token from COSC.
    """
    global _cosc_authentication_token
    if not '_cosc_authentication_token' in globals():
        url = "http://%s:%d/oauth2/token" % (hostname, port)
        print('cosc authentication url:', url)
        form_data = {'grant_type': 'password', 'username': username, 'password':password, 'scope':'sdn'}
        print('cosc authentication parameters:')
        [print('  ',k,'=',v) for (k,v) in form_data.items()]
        try:
            response = post(url, data=form_data, verify=False)
            print('cosc authentication status code:', response.status_code)
            expected_status_code = 201
            if response.status_code == expected_status_code:
                _cosc_authentication_token = response.json()['access_token']
            else:
                msg = 'Expected HTTP status code %s, got %d' % (expected_status_code, response.status_code)
                if response.text:
                    raise ValueError(msg, response.text)
                else:
                    raise ValueError(msg)
        except Exception as e:
            raise ValueError('Unable to obtain COSC authentication token.', url, e)
    return _cosc_authentication_token

