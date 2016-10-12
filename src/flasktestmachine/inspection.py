from bs4 import BeautifulSoup


class HtmlAssertions():

    _soup = None
    html = ''

    @property
    def soup(self):

        if not self._soup:
            self._soup = BeautifulSoup(self.html, 'html.parser')

        return self._soup

    def assert_definition(self, dt_text, dd_text):
        '''
        Asserts that a matching <dd> and <dt> can be found

        :param dt_text: (str): Text to match a <dt> on
        :param dd_text: (str): This text must be in the next <dd>
        '''

        dt = self.soup.find('dt', text=dt_text)
        assert dt, 'No <dt> found with text ' + dt_text
        dd = dt.findNext('dd')
        assert dd, 'No <dd> found after <dt>'
        assert dd.text == dd_text, '<dd> did not match {} was {}'\
            .format(dd_text, dd.text)

    def assert_link(self, text=None, href=None):
        '''
        Asserts that a matching <a> tag is found
        :param text: (str) Text content of the tag
        :param href: (str) Value of the href attribute of the tag
        :return: The <a> that was found
        '''

        kwargs = {}
        if href:
            kwargs['href'] = href

        a = self.soup.find('a', text=text, **kwargs)
        assert a

        return a

    def assert_table(self, id=None, head=None, rows=None, foot=None):
        '''
        Asserts that a matching table is present in the html
        :param id: (str) id attribute for the table
        :param head: (list of list of str) to match to rows in the table head
        :param rows: (list or list of str) to match to rows in teh table body
        :return:
        '''

        if id:
            table = self.soup.find('table', {'id':id})
        else:
            table = self.soup.find('table')

        assert table, 'No table found'

        _assert_table_rows(table.find('thead'), head or [], 'header')
        _assert_table_rows(table.find('tbody'), rows or [], 'body')
        _assert_table_rows(table.find('tfoot'), foot or [], 'footer')

def _assert_table_rows(section, expected, noun):

    if section:
        rows = []
        for tr in section.findAll('tr'):
            data = [td.text.strip() for td in tr.findAll(['th', 'td'])]
            rows.append(data)
    else:
        rows = []

    assert expected == rows
