import logging
import re


import bs4
import requests
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(filename=BASE_DIR / 'url.log', level=logging.INFO)


def get_url_index():
    """get the url of the categories book  from the home page of the website

    Returns:
        list[str]:  contains URLs of index

    """

    r = requests.get( "http://books.toscrape.com/catalogue/category/books_1/index.html" )
    soup = bs4.BeautifulSoup( r.content, 'html.parser' )
    # print(r.status_code)
    links = [str( link.get( 'href' ) ) for link in soup.find_all( 'a' )]
    links = links[3:15]  # 53
    url_index = [link.replace( "../", "http://books.toscrape.com/catalogue/category/" ) for link in links]
    logging.info(f"Generating index url : {url_index}, url number = {len(url_index)}")
    return url_index


def get_url_page(url_index):  # (no books)
    """get all URL for all categorie ex: if the cathegorie have two pages this function will have

    Args:
        url_index (list[str]): contains URLs of index

    Returns:
        (list[str]): list that contains all urls pages of categories

    """

    all_url_without_books = []
    for i in range( 3 ):  # 50
        a = re.match( r".+(_\d|\d([/index.html]))", url_index[i] )
        if a != None:
            all_url_without_books.append( url_index[i] )

        for page in range( 1, 9 ):  # min one page and max 8 pages for one categorie
            url_tested = url_index[i].replace( "index.html", f"page-{page}.html" )

            all_url_without_books.append( url_tested )
    all_url_without_books_clean = []
    for url in all_url_without_books:
        r = requests.get( url )
        if r.ok == True:
            all_url_without_books_clean.append( url )
    all_url_without_books_clean = sorted( list( set( all_url_without_books_clean ) ) )
    # print(all_url_without_books_clean)
    # print(len(all_url_without_books_clean))

    for url in all_url_without_books_clean:
        b = re.match( r".+/page-[1].html", url )
        if b != None:
            all_url_without_books_clean.remove( url )
    # print( all_url_without_books_clean )
    # print( len( all_url_without_books_clean ) )
    logging.info( f"Generating good url : {all_url_without_books_clean}, {len(all_url_without_books_clean)}" )
    return all_url_without_books_clean


def get_url_book(all_url_wthout_books_clean):
    """get all the urls of the books

    Args:
        all_url_wthout_books_clean (list[str]): list that contains all urls pages of categories

    Returns:
        list[str]: url list of books

    """

    url_books = []
    for url in all_url_wthout_books_clean:
        r = requests.get( url )
        soup = bs4.BeautifulSoup( r.content, 'html.parser' )
        h3 = soup.find_all( "h3" )
        # print(a)
        links = []
        # print(h3)
        for h in h3:
            a = h.find( 'a' )
            link = a["href"]
            links.append( str( link ) )

        for i in links:
            a = i.replace( "../../../", "http://books.toscrape.com/catalogue/" )
            url_books.append( a )
    logging.info( f"Generating good url : {url_books}, {len(url_books)} " )
    return url_books


url_index = get_url_index()

all_url_without_books_clean = get_url_page( url_index )

url_books = get_url_book( all_url_without_books_clean )
