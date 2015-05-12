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
        resp = requests.get("{0}{1}".format(tinder_server, uri),
                            headers=headers)
        if resp.status_code >= 300:
            raise requests.HTTPError(status_code=resp.status_code,
                                     reason=resp.reason)
        return json.loads(resp.content)

    def post(self, uri, data, headers={},
             tinder_server="https://api.gotinder.com/"):
        """
        POST some JSON data a Tinder API URI. Returns the decoded JSON response.

        :param uri: URI to GET.
        :param tinder_server: (optional) URL to the Tinder API.
        :param headers: (optional) dictionary of addtional headers to send the
                        Tinder API.
        :param
        :rtype dict:
        """
        headers.update(self.base_headers)
        headers.update({'content-type': 'application/json'})
        data = json.dumps(data)
        req = requests.post("{0}{1}".format(tinder_server, uri),
                            headers=headers, data=data)
        req.raise_for_status()
        return json.loads(req.content)

    def authorize(self, fb_id, fb_token):
        data = {'facebook_token': fb_token,
                 'facebook_id': fb_id}
        resp = self.post('auth', data)
        if 'token' not in resp:
            raise requests.HTTPError('Unable to authorize')
        self.auth_token = resp['token']

    def recommendations(self):
        h = {'X-Auth-Token': self.auth_token}
        resp = self.get('user/recs', headers=h)
        print resp

    def updates(self):
        pass
