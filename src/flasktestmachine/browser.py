from bs4 import BeautifulSoup


class Browser():

    _soup = None

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

        while self.rsp and self.rsp.status_code in [301, 302]:
            self.url = self.rsp.location
            kwargs['method'] = 'GET'

            self.rsp = self.client.open(self.url, *args, **kwargs)

        assert self.rsp.status_code == 200

        return self.rsp

    def submit_form(self, selector, data):

        form = self.soup.find('form', selector)
        assert form, 'Form not found'
        form_data = {}

        for input in form.find_all('input', {'name': True}):
            form_data[input.get('name')] = input.get('value')

        # update the form data with user supplied
        form_data.update(data)

        action = form.get('action') or self.url
        method = form.get('method').upper()

        return self.open(action, method=method, data=form_data)

    @property
    def soup(self):

        assert self.rsp, 'You must send a request to the app before ' \
                          'inspecting the response'

        if not self._soup:
            self._soup = BeautifulSoup(self.rsp.data, 'html.parser')

        return self._soup

    def assert_definition(self, dt_text, dd_text):
        '''
        Asserts that a matching <dd> and <dt> can be found

        Args:
            dt_text (string): Text to match a <dt> on
            dd_text (string): This text must be in the next <dd>
        '''

        dt = self.soup.find('dt', text=dt_text)
        assert dt, 'No <dt> found with text ' + dt_text
        dd = dt.findNext('dd')
        assert dd, 'No <dd> found after <dt>'
        assert dd.text == dd_text, '<dd> did not match {} was {}'\
            .format(dd_text, dd.text)

    def assert_link(self, text=None, href=None):

        a = self.soup.find('a', text=text, href=href)
        assert a