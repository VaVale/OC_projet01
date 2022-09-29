from pprint import pprint
import re

import requests
from bs4 import BeautifulSoup
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

for i in range(11):

    url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    req = requests.get(url, headers)


    soup = BeautifulSoup( req.content, 'html.parser' )
    links_url = soup.find_all("h3")
    links_url = str(links_url)
    links_url = re.split(r' href="| title=',links_url)
    links_url = [str(link).replace("../../../","http://books.toscrape.com/catalogue/").replace('"','') for link in links_url if link.startswith("../../../")]
    links_url =links_url[i]
    print(links_url)

    if req.ok:
        pass



# def extraction():
#     pass
#
# def transformation():
#     pass
#
# def loading():
#     pass