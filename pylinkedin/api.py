import json
import oauth2 as oauth

import endpoints
from exceptions import LinkedInException
from helpers import args_to_dict, build_url_with_qs, date_to_str

class LinkedIn(object):
    def __init__(self, consumer_key=None, consumer_secret=None,
            oauth_key=None, oauth_secret=None):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.token = oauth.Token(oauth_key, oauth_secret)
        self.client = oauth.Client(self.consumer, self.token)

    def get_group_memberships(self):
        url = endpoints.GROUP_MEMBERSHIPS
        return self._make_request(url)

    def get_network_updates(self, update_type=None, before=None, after=None):
        if type(update_type) not in (list, basestring):
            raise TypeError('update_type must be a list or a string')
        if before:
            before = date_to_str(before)
        if after:
            after = date_to_str(after)
        args = args_to_dict(type=update_type, before=before, after=after)
        url = build_url_with_qs(endpoints.NETWORK_UPDATES, args)
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

