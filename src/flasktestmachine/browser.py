# coding: utf-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json

from six.moves.urllib.parse import parse_qsl
from werkzeug.http import parse_cookie

from .inspection import HtmlAssertions


class Browser(HtmlAssertions):

    _soup = None
    html = ''

    def __init__(self, client):
        self.client = client
        self.rsp = None

        self.url = None

        self.environ_base = {}

    def set_user_agent(self, value):
        self.environ_base['HTTP_USER_AGENT'] = value

    def get(self, *args, **kwargs):
        """GET a url from the app"""
        kwargs['method'] = 'GET'
        return self.open(*args, **kwargs)

    def post(self, *args, **kwargs):
        """POST a request to the app"""
        kwargs['method'] = 'POST'
        return self.open(*args, **kwargs)

    def open(self, url, *args, **kwargs):

        # We need to follow redirects ourselves to keep track of the location
        follow_redirects = kwargs.get('follow_redirects', True)
        kwargs['follow_redirects'] = False
        expected_status = kwargs.pop('status', 200)
        kwargs.setdefault('environ_base', self.environ_base)

        self._soup = None
        self.url = url
        self.rsp = self.client.open(url, *args, **kwargs)

        if 'data' in kwargs:
            del kwargs['data']
        if 'query_string' in kwargs:
            del kwargs['query_string']

        if follow_redirects:
            while self.rsp and self.rsp.status_code in [301, 302]:
                self.url = self.rsp.location.replace('http://localhost', '')
                kwargs['method'] = 'GET'

                action, qs = split_url(self.url)
                kwargs['query_string'] = qs

                self.rsp = self.client.open(action, *args, **kwargs)

        assert self.rsp.status_code == expected_status, \
            'Expected {} received {}'.format(expected_status,
                                             self.rsp.status_code)

        cd = self.rsp.headers.get('Content-Disposition') or ''
        if cd.startswith('attachment'):
            self.json = None
            self.html = None

        elif self.rsp.content_type == 'application/json':
            self.json = json.loads(self.rsp.data)
            self.html = None
        else:
            self.json = None
            self.html = self.rsp.data

        return self.rsp

    def submit_form(self, selector, data, **kwargs):
        """
        Submits the form, found in the html identified by selector to the app.
        All form values in the html are sent along with any values
        in the data param
        :param selector: (dict) values to find the form
        :param data: (dict) additional data to post with the form
        :return:
        """

        form = self.soup.find('form', selector)
        assert form, 'Form not found'

        form_data = {}
        form_data.update(self._get_form_input_values(form))
        form_data.update(self._get_form_select_values(form))

        # update the form data with user supplied
        for k, v in data.iteritems():
            if v is None:
                del form_data[k]
            else:
                form_data[k] = v

        action, query_string = split_url(form.get('action') or self.url)
        method = form.get('method').upper()

        if method == 'GET':
            for k, v in form_data.iteritems():
                query_string.append((k, v))
            return self.open(action, method='GET',
                             query_string=query_string,
                             **kwargs)

        return self.open(action, method=method,
                         data=form_data,
                         query_string=query_string,
                         **kwargs)

    def _get_form_input_values(self, form):
        rv = {}
        for input in form.find_all('input', {'name': True}):
            if input.get('type') in ('checkbox', 'radio'):
                if 'checked' in input.attrs:
                    rv[input.get('name')] = input.get('value')
            else:
                rv[input.get('name')] = input.get('value')
        return rv

    def _get_form_select_values(self, form):
        rv = {}
        for select in form.find_all('select', {'name': True}):
            for i, option in enumerate(select.find_all('option')):
                if i == 0 or 'selected' in option.attrs:
                    rv[select.get('name')] = option.get('value')
        return rv

    def follow_link(self, text=None, href=None, **kwargs):
        """
        Assert that a <a> tag exists containing text (if set)
        with href href (if set), then sends a get request
        to the specified url
        :param text: (str) Text content of teh tag
        :param href: (str) Value of the href attribute of the tag
        :return: None
        """

        a = self.assert_link(text=text, href=href)

        self.get(a['href'], **kwargs)

    def get_cookie(self, name):
        cookies = self.rsp.headers.getlist('Set-Cookie')
        for cookie in cookies:
            c_key, c_value = parse_cookie(cookie).items()[0]
            if c_key == name:
                return c_value
        return None


def split_url(url):
    if '?' in url:
        action, qs = url.split('?')
        query_string = parse_qsl(qs, keep_blank_values=True)
        return action, query_string

    return url, []
