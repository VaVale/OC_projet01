import logging
import re

import bs4
import requests
from pathlib import Path

BASE_DIR = Path( __file__ ).resolve().parent
logging.basicConfig( filename=BASE_DIR / 'link.log', level=logging.INFO )


def get_url_index():
    """get the link of the categories book  from the home page of the website

    Returns:
        p list[str]:  contains URLs of index

    """

    r = requests.get( "http://books.toscrape.com/catalogue/category/books_1/index.html" )
    soup = bs4.BeautifulSoup( r.content, 'html.parser' )
    links = [str( link.get( 'href' ) ) for link in soup.find_all( 'a' )]
    links = links[3:53]  # 53
    list_url_index = [link.replace( "../", "http://books.toscrape.com/catalogue/category/" ) for link in links]
    logging.info( f"Generating index link : {list_url_index}, link number = {len( list_url_index )}" )
    return list_url_index


def get_url_page():  # (no books)
    """get all URL for all categorie ex: if the cathegorie have two pages this function will have

    Returns:
        (list[str]): list that contains all urls pages of categories

    """

    all_url_without_books = []
    for i in range( 50 ):  # 50
        a = re.match( r".+(_\d|\d([/index.html]))", url_index[i] )
        if a is not None:
            all_url_without_books.append( url_index[i] )

        for page in range( 1, 9 ):  # min one page and max 8 pages for one categorie
            url_tested = url_index[i].replace( "index.html", f"page-{page}.html" )

            all_url_without_books.append( url_tested )
    urls_clean = []
    for url in all_url_without_books:
        r = requests.get( url )
        if r.ok:
            urls_clean.append( url )
    urls_clean = sorted( list( set( urls_clean ) ) )

    for url in urls_clean:
        b = re.match( r".+/page-'1'.html", url )
        if b is not None:
            urls_clean.remove( url )
    logging.info( f"Generating good u : {urls_clean}, {len( urls_clean )}" )
    return urls_clean


def get_url_book(all_url_wthout_books_clean):
    """get all the urls of the books

    Args:
        all_url_wthout_books_clean (list[str]): list that contains all urls pages of categories

    Returns:
        list[str]: u list of books

    """

    books = []
    for url in all_url_wthout_books_clean:
        r = requests.get( url )
        soup = bs4.BeautifulSoup( r.content, 'html.parser' )
        h3 = soup.find_all( "h3" )
        links = []
        for h in h3:
            a = h.find( 'a' )
            link = a["href"]
            links.append( str( link ) )

        for i in links:
            a = i.replace( "../../../", "http://books.toscrape.com/catalogue/" )
            books.append( a )
    logging.info( f"Generating good u : {books}, {len( books )} " )
    return books


url_index = get_url_index()

all_url_without_books_clean = get_url_page()

url_books = get_url_book( all_url_without_books_clean )
