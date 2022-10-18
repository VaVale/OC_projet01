import re

import requests
from bs4 import BeautifulSoup


def get_url_index():
    r = requests.get( "http://books.toscrape.com/catalogue/category/books_1/index.html" )
    soup = BeautifulSoup( r.content, 'html.parser' )
    # print(r.status_code)
    links = [str( link.get( 'href' ) ) for link in soup.find_all( 'a' )]
    links = links[3:53]  # 53
    url_index = [link.replace( "../", "http://books.toscrape.com/catalogue/category/" ) for link in links]

    return url_index


def get_url_page(url_index):  # for get all index url (no books)
    all_url_without_books = []
    for i in range( 50 ):  # 50
        a = re.match( r".+(_\d|\d([/index.html]))", url_index[i] )
        if a != None:
            all_url_without_books.append( url_index[i] )

        for page in range( 1, 9 ):
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

    return all_url_without_books_clean


def get_url_book(all_url_wthout_books_clean):
    url_books = []
    for url in all_url_wthout_books_clean:
        r = requests.get( url )
        soup = BeautifulSoup( r.content, 'html.parser' )
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

    return url_books


url_index = get_url_index()

all_url_without_books_clean = get_url_page( url_index )

url_books = get_url_book( all_url_without_books_clean )

# print(url_books)


# with open( 'urls.txt', 'w' ) as f:
#     for link in url_books:
#         f.write( link + '\n' )
