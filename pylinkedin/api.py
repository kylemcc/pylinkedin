import json
import oauth2 as oauth

import endpoints
from exceptions import LinkedInException

class LinkedIn(object):
    def __init__(self, consumer_key=None, consumer_secret=None,
            oauth_key=None, oauth_secret=None):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.token = oauth.Token(oauth_key, oauth_secret)
        self.client = oauth.Client(self.consumer, self.token)

    def get_group_memberships(self):
        url = endpoints.GROUP_MEMBERSHIPS
        return self._make_request(url)

    def _make_request(self, uri, method='GET', body=None):
        headers = {'x-li-format': 'json'}
        if method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json'
        resp, content = self.client.request(uri, method=method,
                headers=headers)
        if resp['status'] == '200':
            return json.loads(content)
        else:
            #TODO: more sophisticated error handling
            raise LinkedInException('API call failed with status: %s' %
                    resp['status'])

