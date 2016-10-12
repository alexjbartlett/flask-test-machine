from inspection import HtmlAssertions
import json


class Browser(object, HtmlAssertions):

    _soup = None
    html = ''

    def __init__(self, client):
        self.client = client
        self.rsp = None

        self.url = None

    def get(self, *args, **kwargs):
        '''GET a url from the app'''
        kwargs['method'] = 'GET'
        return self.open(*args, **kwargs)

    def post(self, *args, **kwargs):
        '''POST a request to the app'''
        kwargs['method'] = 'POST'
        return self.open(*args, **kwargs)

    def open(self, url, *args, **kwargs):

        # We need to follow redirects ourselves to keep track of the location
        kwargs['follow_redirects'] = False

        self._soup = None
        self.url = url
        self.rsp = self.client.open(url, *args, **kwargs)

        if 'data' in kwargs:
            del kwargs['data']

        while self.rsp and self.rsp.status_code in [301, 302]:
            self.url = self.rsp.location
            kwargs['method'] = 'GET'

            self.rsp = self.client.open(self.url, *args, **kwargs)

        assert self.rsp.status_code == 200

        if self.rsp.content_type == 'application/json':
            self.json = json.loads(self.rsp.data)
            self.html = None
        else:
            self.json = None
            self.html = self.rsp.data

        return self.rsp

    def submit_form(self, selector, data):
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

        for input in form.find_all('input', {'name': True}):
            form_data[input.get('name')] = input.get('value')

        # update the form data with user supplied
        form_data.update(data)

        action = form.get('action') or self.url
        method = form.get('method').upper()

        if method == 'GET':
            return self.open(action, method='GET', query_string=form_data)

        return self.open(action, method=method, data=form_data)

    def follow_link(self, text=None, href=None):
        """
        Assert that a <a> tag exists containing text (if set)
        with href href (if set), then sends a get request
        to the specified url
        :param text: (str) Text content of teh tag
        :param href: (str) Value of the href attribute of the tag
        :return: None
        """

        a = self.assert_link(text=text, href=href)

        self.get(a['href'])
