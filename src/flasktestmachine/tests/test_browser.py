from flasktestmachine.browser import  Browser
import json


class _Response():

    def __init__(self, status_code, data,
                 location=None,
                 content_type='text/html'):

        self.status_code = status_code
        self.data = data
        self.location = location
        self.content_type = content_type


class _JsonResponse():

    def __init__(self, status_code, data):

        self.status_code = status_code
        self.data = json.dumps(data)
        self.content_type = 'application/json'


def test_get():

    class Client():

        def open(self, url, *args, **kwargs):
            assert url == '/abcdefg'
            assert kwargs.get('method') == 'GET'
            assert kwargs.get('follow_redirects') == False

            return _Response(200, '')

    subject = Browser(Client())

    subject.get('/abcdefg')


def test_post():

    class Client():

        def open(self, url, *args, **kwargs):
            assert url == '/abcdefg'
            assert kwargs.get('method') == 'POST'
            assert kwargs.get('follow_redirects') == False
            assert kwargs.get('data') == {'key': 'value'}

            return _Response(200, '')

    subject = Browser(Client())

    subject.post('/abcdefg', data={'key': 'value'})


def test_json_response():

    class Client():

        def open(self, url, *args, **kwargs):
            assert url == '/jsonendpoint'
            assert kwargs.get('method') == 'POST'

            return _JsonResponse(200, {'value': 7})

    subject = Browser(Client())

    subject.post('/jsonendpoint')

    assert subject.json == {'value': 7}


def test_submit_form():

    class Client():

        def open(self, url, *args, **kwargs):
            assert url == '/xyz'
            assert kwargs.get('method') == 'POST'
            assert kwargs.get('follow_redirects') == False
            assert kwargs.get('data') == {'key': 'value', 'x': 'y'}

            return _Response(200, 'Success')

    subject = Browser(Client())
    subject.url = '/xyz'
    subject.html = """
        <html>
            <form method="post">
                <input type="text" name="key" value="value" />
                <input type="text" name="x" value="" />
            </form>
        </html>
    """

    subject.submit_form({}, {'x': 'y'})

    assert subject.html == 'Success'


def test_follow_link():

    class Client():

        def open(self, url, *args, **kwargs):
            assert url == '/right'
            assert kwargs.get('method') == 'GET'
            assert kwargs.get('follow_redirects') == False

            return _Response(200, 'Sent OK')

    subject = Browser(Client())
    subject.url = '/xyz'
    subject.html = """
        <html><body>
            <a href="/right" >The One</a>
            <a href="/wrong" >Not The One</a>
        </body></html>
    """

    subject.follow_link(text='The One')

    assert subject.html == 'Sent OK'