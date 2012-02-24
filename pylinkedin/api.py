import json
import oauth2 as oauth

import endpoints

class LinkedIn(object):
    def __init__(self, consumer_key=None, consumer_secret=None,
            oauth_token=None, oauth_secret=None):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.token = oauth.Token(oauth_token, oauth_secret)
        self.client = oauth.Client(self.consumer, self.token)

    def get_groups(self):
        url = endpoints.GROUP_MEMBERSHIPS
        headers = {'x-li-format': 'json'}
        resp, content = self.client.request(url, headers=headers)
        if resp['status'] == '200':
            return json.loads(content)
        else:
            raise Exception('Could not fetch groups')
