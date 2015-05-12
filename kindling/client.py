# -*- coding: utf-8 -*-

# (The MIT License)
#
# Copyright (c) 2015 Kura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import json
import requests


class Client(object):
    auth_token = None
    base_headers = {'app_version': 3, 'platform': 'ios',
                    'user-agent': 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)'}

    def _get(self, uri, headers={}, tinder_server="https://api.gotinder.com/"):
        """
        GET a URI from the Tinder API. Returns the decoded JSON response.

        :param uri: URI to GET.
        :param tinder_server: (optional) URL to the Tinder API.
        :param headers: (optional) dictionary of addtional headers to send the
                        Tinder API.
        :rtype dict:
        """
        headers.update(self.base_headers)
        headers.update({'content-type': 'application/json'})
        if self.auth_token:
            headers.update({'X-Auth-Token': self.auth_token})
        resp = requests.get("{0}{1}".format(tinder_server, uri),
                            headers=headers)
        if resp.status_code >= 300:
            raise requests.HTTPError(status_code=resp.status_code,
                                     reason=resp.reason)
        return json.loads(resp.content)

    def _post(self, uri, data, headers={},
             tinder_server="https://api.gotinder.com/"):
        """
        POST some JSON data a Tinder API URI. Returns the decoded JSON
        response.

        :param uri: URI to GET.
        :param data: dictionary of data to send.
        :param tinder_server: (optional) URL to the Tinder API.
        :param headers: (optional) dictionary of addtional headers to send the
                        Tinder API.
        :rtype dict:
        """
        headers.update(self.base_headers)
        headers.update({'content-type': 'application/json'})
        if self.auth_token:
            headers.update({'X-Auth-Token': self.auth_token})
        req = requests.post("{0}{1}".format(tinder_server, uri),
                            headers=headers, data=json.dumps(data))
        req.raise_for_status()
        return json.loads(req.content)

    def authorize(self, fb_id, fb_token):
        """
        Authorize with Tinder.

        :param fb_id: Facebook user ID.
        :param fb_token: Facebook auth token.
        :rtype bool:
        """
        data = {'facebook_token': fb_token,
                'facebook_id': fb_id}
        resp = self._post('auth', data)
        if 'token' not in resp:
            raise requests.HTTPError('Unable to authorize')
        self.auth_token = resp['token']
        return True

    def update_profile(self, gender, min_age, max_age, distance):
        """
        Update your Tinder profile.

        :param gender: 0 for male, 1 for female, -1 for both.
        :param min_age: minimum age for matches.
        :param max_age: maximum age for matches.
        :param distance: max search radius in kilometers.
        :type bool:
        """
        if gender not in (-1, 0, 1):
            return False
        data = {'gender': gender, 'age_filter_min': min_age,
                'age_filter_max': max_age, 'distance_filter': distance}
        resp = self._post('profile', data=data)
        if 'interests' in resp:
            return True
        return False

    def update_location(self, latitude, longitude):
        """
        Update your location using latitude and longitude.

        :param latitude:
        :param longitude:
        :rtype dict:
        """
        return self._post('user/ping', {'lat': latitude, 'lon': longitude})

    def report_user(self, user_id, reason):
        """
        Report a user.

        :param user_id:
        :param reason: 1 for spam, 2 for inappropriate/offensive.
        :rtype dict:
        """
        if reason not in (1, 2):
            return False
        return self._post('report/{0}'.format(user_id), {'cause': reason})

    def send_message(self, user_id, message):
        """
        Send user a message. Will not work if user is not a match.

        :param user_id: ID of user to send the message.
        :param message: Message to send.
        :rtype dict:
        """
        return self._post('user/matches/{0}'.format(user_id), {'message': message})

    def _like_unlike(self, action, user_id):
        if action not in ('like', 'unlike'):
            return False
        return self._get("{0}/{1}".format(action, user_id))

    def like(self, user_id):
        """
        Like/Swipe right a user.

        :param user_id: User ID to Like/Match.
        :rtype dict:
        """
        return self._like_pass('like', user_id)

    def unlike(self, user_id):
        """
        Unlike/Pass/Swipe left a user.

        :param user_id: User to Unlike/Pass/Swipe left.
        :rtype dict:
        """
        return self._like_pass('unlike', user_id)

    @property
    def recommendations(self):
        """
        Recommendations. TODO: update with specifics.

        :rtype dict:
        """
        return self._get('user/recs')

    @property
    def updates(self):
        """
        Updates. TODO: update with specifics.

        :rtype dict:
        """
        return self._get('updates')
