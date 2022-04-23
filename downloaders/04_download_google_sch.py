#!/usr/bin/env python3

# TODO: Can use 'scholarly' python module
# (but it has A LOT of extra dependencies)

# NOTE: Google Scholar has no official API.
# There is freemium service SERP API that can be used
# to run 100 Google Scholar queries per month.

# Useful helper functions for parsing the webpage:
# https://dev.to/dmitryzub/scrape-google-scholar-with-python-32oh#author_articles

################################################
# NOTE: The current solution does not work
# with LaTeX formulae.
# TODO: Might be able to fix it by manually getting citation data for each article:
# https://scholar.google.com/scholar.bib?q=info:sAn93W8TBY8J:scholar.google.com/&output=cite&scirp=0&hl=en
# (didn't seem to work. IDs on author page and in citation queries are different)
#
# For now it is recommended to export citations
# manually, using Select All -> Export ->
# -> CSV
################################################


raise NotImplementedError("""
This script is not finished. For now
it is recommended to export citations
manually, using Select All -> Export -> CSV
""")

import requests
from lxml import etree

# urls = open('config.txt', 'r').readlines()

author_id = 'v9pTs7IAAAAJ'
url = f'https://scholar.google.com/citations?user={author_id}&hl=en'

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +\
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 " +\
    "Safari/537.36 Edge/18.19582"
}

params = {
   "user": author_id,
   "sortby": "pubdate",
   "hl": "en"
}

def get_articles():
    """From https://dev.to/dmitryzub/scrape-google-scholar-with-python-32oh#author_articles
    """
    html = requests.get('https://scholar.google.com/citations', headers=headers, params=params).text
    tree = etree.fromstring(html, etree.HTMLParser())

    # print_html(html)

    for i in range(20):
        print()
    print('Article info:')
    # cells = tree.xpath('//tbody[@id = "gsc_a_b"]')
    cells = tree.xpath('//tbody[@id = "gsc_a_b"]/tr/td[@class = "gsc_a_t"]')
    for article_info in cells:
        print(etree.tostring(article_info, pretty_print=True, encoding='unicode'))
        title_elem = article_info.find('./*[@class = "gsc_a_at"]')
        title = ' '.join(title_elem.itertext())

        title_link = 'https://scholar.google.com/' + title_elem.get('href')
        authors = article_info.find('./div[1]').text
        publications = article_info.find('./div[2]').text
        print(f'Title: {title}\nTitle link: {title_link}\nArticle Author(s): {authors}\nArticle Publication(s): {publications}\n')
    # for article_info in soup.select('#gsc_a_b .gsc_a_t'):
    #     title = article_info.select_one('.gsc_a_at').text
    #     title_link = f"https://scholar.google.com{article_info.select_one('.gsc_a_at')['href']}"
    #     authors = article_info.select_one('.gsc_a_at+ .gs_gray').text
    #     publications = article_info.select_one('.gs_gray+ .gs_gray').text

    #     print(f'Title: {title}\nTitle link: {title_link}\nArticle Author(s): {authors}\nArticle Publication(s): {publications}\n')


def print_html(content):
    """Simple print page as html helper function."""
    content = '<root>' + content + '</root>'
    tree = etree.fromstring(content, etree.HTMLParser())
    print(etree.tostring(tree, pretty_print=True, encoding='unicode'))

get_articles()

