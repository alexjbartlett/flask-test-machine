from flasktestmachine.browser import  Browser


class _Response():

    def __init__(self, status_code, data, location=None):
        self.status_code = status_code
        self.data = data
        self.location = location

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