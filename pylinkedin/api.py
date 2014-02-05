import json
import requests

from functools import partial

import endpoints

from .exceptions import LinkedInException
from helpers import date_to_str
from .oauth import OAuth

PROFILE_ARGS = ','.join(['first-name','last-name','id','picture-url','public-profile-url'])

class BaseResponse(object):
    def __init__(self, response):
        self.response = response

    @property
    def headers(self):
        return self.response.headers

    @property
    def status_code(self):
        return self.response.status_code

class CreatedResponse(BaseResponse):
    def __str__(self):
        return 'Created'

    def __nonzero__(self):
        return True

class NoContentResponse(BaseResponse):
    def __str__(self):
        return 'No Content'

    def __nonzero__(self):
        return True

class LinkedIn(object):
    def __init__(self, auth=None, request_timeout=None, proxies=None,
            headers=None):
        self.auth = None
        self.request_timeout = request_timeout
        self.proxies = proxies
        self.auth = auth
        self.headers = headers or {}

    def get_group_memberships(self):
        url = endpoints.GROUP_MEMBERSHIPS
        return self._make_request(url)

    def get_group_posts(self, group_id, start=0, count=10, order='recency',
            role=None, modified_since=None, **kwargs):
        if order not in ('recency', 'popularity'):
            raise ValueError('Sort order must be either recency or popularity')

        url = endpoints.GROUP_FEED.format(group_id=group_id)
        kwargs['modified-since'] = modified_since
        return self._make_request(
                url,
                start=start,
                count=count,
                order=order,
                role=role,
                **kwargs)

    def create_group_post(self, group_id, title, summary, **kwargs):
        url = endpoints.CREATE_POST.format(group_id=group_id)
        return self._make_request(
                url,
                method='POST',
                title=title,
                summary=summary,
                **kwargs)

    def delete_group_post(self, post_id, **kwargs):
        url = endpoints.DELETE_POST.format(post_id=post_id)
        return self._make_request(url, method='DELETE', **kwargs)

    def get_comments_for_post(self, post_id, count=10, start=0, **kwargs):
        url = endpoints.POST_COMMENTS.format(post_id=post_id)
        return self._make_request(url, count=count, start=start, **kwargs)

    def create_comment(self, post_id, text):
        url = endpoints.CREATE_COMMENT.format(post_id=post_id, **kwargs)
        return self._make_request(url, method='POST', text=text, **kwargs)

    def delete_comment(self, comment_id, **kwargs):
        url = endpoints.DELETE_COMMENT.format(comment_id=comment_id)
        return self._make_request(url, method='DELETE', **kwargs)

    def like_post(self, post_id, **kwargs):
        return self._like_unlike_post(post_id, True, **kwargs)

    def unlike_post(self, post_id, **kwargs):
        return self._like_unlike_post(post_id, False, **kwargs)

    def _like_unlike_post(self, post_id, is_liked, **kwargs):
        body = json.dumps(is_liked) #json true/false
        url = endpoints.LIKE_POST.format(post_id=post_id)
        return self._make_request(url, method='PUT', body=body, **kwargs)

    def get_network_updates(self, update_type=None, before=None, after=None,
            count=10, start=0, **kwargs):
        update_type = update_type or []
        if not isinstance(update_type, (list, tuple, basestring)):
            raise TypeError('update_type must be a list or a string')
        if before:
            before = date_to_str(before)
        if after:
            after = date_to_str(after)

        url = endpoints.NETWORK_UPDATES
        return self._make_request(
                url,
                type=update_type,
                before=before,
                after=after,
                count=count,
                start=start,
                **kwargs)

    def get_profile(self, member_id=None):
        if member_id is None:
            url = "%s/~:(%s)" % (endpoints.PROFILE, PROFILE_ARGS)
        else:
            url = "%s/id=%s:(%s)" % (endpoints.PROFILE, member_id, PROFILE_ARGS)
        return self._make_request(url)

    def _make_request(self, uri, method='GET', headers=None, body=None,
            _timeout=None, **kwargs):
        headers = headers or {}
        headers['x-li-format'] = 'json'

        timeout = _timeout or self.request_timeout

        if method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json'
            data = body or json.dumps(kwargs)
            request = partial(requests.request, data=data)
        else:
            request = partial(requests.request, params=kwargs)

        resp = request(
                method,
                uri,
                headers=headers,
                timeout=timeout,
                proxies=self.proxies,
                auth=self.auth)
        try:
            return self._handle_response(resp)
        except requests.exceptions.HTTPError as e:
            raise LinkedInException(
                    cause=e,
                    status_code=resp.status_code,
                    response=resp)

    def _handle_response(self, resp):
        resp.raise_for_status()
        content_type = resp.headers.get('Content-Type', '')
        i = content_type.find(';')
        if i > 0:
            content_type = content_type[:i]

        if content_type == 'application/json':
            return self._create_response(resp, json.loads(resp.content))
        elif resp.status_code == 201:
            return CreatedResponse(resp)
        elif resp.status_code == 204:
            return NoContentResponse(resp)
        return self._create_response(resp, resp.content)

    def _create_response(self, response, content):
        resp_type = type(content) if type(content) != bool else int
        class R(resp_type, BaseResponse):
            def __new__(cls, response, content):
                return resp_type.__new__(cls, content)

            def __init__(self, response, content):
                resp_type.__init__(content)
                BaseResponse.__init__(response)
