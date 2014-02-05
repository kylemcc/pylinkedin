Usage
=====

>>> import pylinkedin
>>> auth = pylinkedin.OAuth(consumer_key='XXX', consumer_secret='XXX', oauth_key='XXX', oauth_secret='XXX')
>>> api = pylinkedin.LinkedIn(auth=auth)
>>> api.get_group_memberships()
