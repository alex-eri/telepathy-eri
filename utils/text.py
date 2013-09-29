__author__ = 'eri'

try:
    import lxml.html
    def striphtml(html):
        t = lxml.html.fromstring(html.replace('<br>','\n'))
        return t.text_content()

except ImportError:
    def striphtml(html):
        return html.replace('<br>','\n')
