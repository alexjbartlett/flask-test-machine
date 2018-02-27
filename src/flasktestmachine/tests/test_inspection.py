from __future__ import absolute_import

import pytest
from flasktestmachine.inspection import HtmlAssertions


def test_assert_link():
    h = HtmlAssertions()
    h.html = '<html><a href="/abc">Some Text</a></html>'

    h.assert_link(text='Some Text', href='/abc')


def test_assert_link_by_text():
    h = HtmlAssertions()
    h.html = '<html><a href="/abc">Some Text</a></html>'

    h.assert_link(text='Some Text')


def test_assert_link_fail_wrong_text():
    h = HtmlAssertions()
    h.html = '<html><a href="/abc">Some Text</a></html>'

    with pytest.raises(AssertionError):
        h.assert_link(text='Wrong Text', href='/abc')


def test_assert_link_fail_wrong_href():
    h = HtmlAssertions()
    h.html = '<html><a href="/abc">Some Text</a></html>'

    with pytest.raises(AssertionError):
        h.assert_link(text='Some Text', href='/xyz')


def test_assert_definition():
    h = HtmlAssertions()
    h.html = '<html><dl><dt>Term</dt><dd>Def</dd></dl></html>'

    h.assert_definition('Term', 'Def')


def test_assert_definition_wrong_term():
    h = HtmlAssertions()
    h.html = '<html><dl><dt>Term</dt><dd>Def</dd></dl></html>'

    with pytest.raises(AssertionError):
        h.assert_definition('Wrong Term', 'Def')


def test_assert_definition_wrong_definition():
    h = HtmlAssertions()
    h.html = '<html><dl><dt>Term</dt><dd>Def</dd></dl></html>'

    with pytest.raises(AssertionError):
        h.assert_definition('Term', 'Wrong Def')


def test_assert_table():
    h = HtmlAssertions()
    h.html = (
        '<html>'
        '    <table>'
        '        <thead>'
        '            <tr><th>H1</th><th>H2</th></tr>'
        '        </thead>'
        '        <tbody>'
        '            <tr><td>R1D1</td><td>R1D2</td></tr>'
        '            <tr><td>R2D1</td><td>R2D2</td></tr>'
        '         </tbody>'
        '    </table>'
        '</html>')

    h.assert_table(head=[['H1', 'H2']],
                   rows=[['R1D1', 'R1D2'],
                         ['R2D1', 'R2D2']])


def test_assert_table_missing_head_row():
    h = HtmlAssertions()
    h.html = (
        '<html>'
        '    <table>'
        '        <thead>'
        '        </thead>'
        '        <tbody>'
        '            <tr><td>R1D1</td><td>R1D2</td></tr>'
        '            <tr><td>R2D1</td><td>R2D2</td></tr>'
        '         </tbody>'
        '    </table>'
        '</html>')

    with pytest.raises(AssertionError):
        h.assert_table(head=[['H1', 'H2']],
                       rows=[['R1D1', 'R1D2'],
                             ['R2D1', 'R2D2']])


def test_assert_table_missing_head_cell():
    h = HtmlAssertions()
    h.html = (
        '<html>'
        '    <table>'
        '        <thead>'
        '            <tr><th>H1</th></tr>'
        '        </thead>'
        '        <tbody>'
        '            <tr><td>R1D1</td><td>R1D2</td></tr>'
        '            <tr><td>R2D1</td><td>R2D2</td></tr>'
        '         </tbody>'
        '    </table>'
        '</html>')

    with pytest.raises(AssertionError):
        h.assert_table(head=[['H1', 'H2']],
                       rows=[['R1D1', 'R1D2'],
                             ['R2D1', 'R2D2']])


def test_assert_table_wrong_head_cell():
    h = HtmlAssertions()
    h.html = (
        '<html>'
        '    <table>'
        '        <thead>'
        '            <tr><th>H1</th><th>Wrong</th></tr>'
        '        </thead>'
        '        <tbody>'
        '            <tr><td>R1D1</td><td>R1D2</td></tr>'
        '            <tr><td>R2D1</td><td>R2D2</td></tr>'
        '         </tbody>'
        '    </table>'
        '</html>')

    with pytest.raises(AssertionError):
        h.assert_table(head=[['H1', 'H2']],
                       rows=[['R1D1', 'R1D2'],
                             ['R2D1', 'R2D2']])


def test_assert_table_wrong_body_cell():
    h = HtmlAssertions()
    h.html = (
        '<html>'
        '    <table>'
        '        <thead>'
        '            <tr><th>H1</th><th>H2</th></tr>'
        '        </thead>'
        '        <tbody>'
        '            <tr><td>R1D1</td><td>R1D2</td></tr>'
        '            <tr><td>R2D1</td><td>C3P0</td></tr>'
        '         </tbody>'
        '    </table>'
        '</html>')

    with pytest.raises(AssertionError):
        h.assert_table(head=[['H1', 'H2']],
                       rows=[['R1D1', 'R1D2'],
                             ['R2D1', 'R2D2']])



def test_assert_table_wrong_footer_cell():
    h = HtmlAssertions()
    h.html = (
        '<html>'
        '    <table>'
        '        <thead>'
        '            <tr><th>H1</th><th>H2</th></tr>'
        '        </thead>'
        '        <tbody>'
        '            <tr><td>R1D1</td><td>R1D2</td></tr>'
        '            <tr><td>R2D1</td><td>R2D2</td></tr>'
        '         </tbody>'
        '        <tfoot>'
        '            <tr><th>F1</th><th>Wrong</th></tr>'
        '        </tfoot>'
        '    </table>'
        '</html>')

    with pytest.raises(AssertionError):
        h.assert_table(head=[['H1', 'H2']],
                       rows=[['R1D1', 'R1D2'],
                             ['R2D1', 'R2D2']],
                       foot=[['F1', 'F2']])