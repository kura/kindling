import json
import requests


class Client(object):
    auth_token = None
    base_headers = {'app_version': 3, 'platform': 'ios'}

    def get(self, uri, headers={}, tinder_server="https://api.gotinder.com/"):
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

    def post(self, uri, data, headers={},
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
        print uri
        print headers
        print data
        req = requests.post("{0}{1}".format(tinder_server, uri),
                            headers=headers, data=json.dumps(data))
        req.raise_for_status()
        return json.loads(req.content)

    def authorize(self, fb_id, fb_token):
        data = {'facebook_token': fb_token,
                 'facebook_id': fb_id}
        resp = self.post('auth', data)
        if 'token' not in resp:
            raise requests.HTTPError('Unable to authorize')
        self.auth_token = resp['token']

    def update_profile(self, gender, min_age, max_age, distance):
        """
        Update your Tinder profile.

        :param gender: 0 for male, 1 for female.
        :param min_age: minimum age for matches.
        :param max_age: maximum age for matches.
        :param distance: max search radius in kilometers.
        :type bool:
        """
        data = {'gender': gender, 'age_filter_min': min_age,
                'age_filter_max': max_age, 'distance_filter': distance}
        resp = self.post('profile', data=data)
        if 'interests' in resp:
            return True
        return False

    def report_user(self, user_id, reason):
        """
        Report a user.

        :param user_id:
        :param reason: 1 for spam, 2 for inappropriate/offensive.
        """
        if reason not in (1, 2):
            return False
        self.post('report/{0}'.format(user_id), {'cause': reason})


    def recommendations(self):
        resp = self.get('user/recs')
        print resp

    def updates(self):
        pass
