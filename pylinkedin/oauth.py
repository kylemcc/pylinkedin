import requests_oauthlib

class OAuth(requests_oauthlib.OAuth1):
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        super(OAuth, self).__init__(
                client_key=consumer_key,
                client_secret=consumer_secret,
                resource_owner_key=oauth_token,
                resource_owner_secret=oauth_secret)

# TODO: OAuth2
