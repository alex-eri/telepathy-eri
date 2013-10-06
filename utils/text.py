import urllib

__author__ = 'eri'

from decorators import logger

try:

    import lxml.html
    import lxml.etree

    def striphtml(html):
        t =  html.replace('<br>','\n')
        try:
            dom = lxml.html.fromstring(t)
            t = dom.text_content()
        except lxml.etree.XMLSyntaxError as e:
            logger.warning(repr(e.message))
            pass

        return t

except ImportError:
    def striphtml(html):
        return html.replace('<br>','\n')


def escape_as_dbus_path(str):
    return urllib.quote(str)
