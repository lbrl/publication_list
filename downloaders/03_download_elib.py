#!/usr/bin/env python3

import requests
from lxml import etree

author_id = 989757

def main():
    ### Download 
    data = load(author_id)
    tree = etree.fromstring(data, etree.HTMLParser())

    rows = tree.xpath('//table/tr[@valign="middle"]')
    out_file = open('elibrary.csv', 'w')

    for row in rows:
        columns = [x.strip() for x in row.itertext()]
        num = columns[1]
        title = columns[4]
        authors = columns[5]
        source = columns[6]
        citations = columns[7]
        out_file.write('"%s","%s","%s"\n' % (title, authors, source))
        print('"%s","%s","%s"' % (title, authors, source))
        # print( '  ;  '.join([num, title, authors, source]) )


def load(author_id):
    """Load data from elibrary
    """
    url1 = f'https://www.elibrary.ru/author_items.asp?authorid={author_id}'
    
    headers = { 'User-Agent': 'Mozilla/5.0' }
    sess = requests.Session()
    sess.headers = headers
    sess.get(url1)
    
    url2 = f'https://elibrary.ru/author_items_print.asp?target=author_items_print{author_id}'
    
    data = sess.get(url2).text
    return data


def print_html(content):
    """Simple print page as html helper function."""
    content = '<root>' + content + '</root>'
    tree = etree.fromstring(content, etree.XMLParser(
        strip_cdata=False, # https://stackoverflow.com/a/25813863
        recover=True))
    print(etree.tostring(tree, pretty_print=True, encoding='unicode'))

################################################

if __name__ == '__main__':
    main()

