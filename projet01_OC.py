import csv
import logging
import os
import re
import string
import urllib.request
from pathlib import Path

import requests
from PIL import Image
from bs4 import BeautifulSoup

from url import url_books

BASE_DIR = Path( __file__ ).resolve().parent
logging.basicConfig( filename=BASE_DIR / 'projet01_OC.log', level=logging.INFO )

for url in range( len( url_books ) ):  # len(books)

    def extract(books):
        """scrape the page web of books

        Args:
            books(str):

        Returns:
            scraped web page

        """
        r = requests.get( books )
        if r.status_code != 200:
            logging.debug( f"PROBLEME URL : {r.status_code}" )
        beauti = BeautifulSoup( r.content, 'html.parser' )

        return beauti


    def transform(s, u):
        """get datas for books
        Args:
            s(soup):scraped web page
            u(str):u of a book

        Returns:
            all datas for books

        """
        csv_header = ("product page u", "universal product code (upc)", "title",
                      "price excluding tax", "price including tax", "number available",
                      "product description", "category", "review rating", "image u")
        value = [u]

        h1 = s.find( "h1" ).text
        h1 = "".join( [i for i in h1 if i not in string.punctuation] )
        data_value = s.find_all( 'td' )
        upc = data_value[0].text
        value.append( upc )
        value.append( h1 )
        price_exclu_tax = data_value[2].text
        price_inclu_tax = data_value[3].text
        value.append( price_exclu_tax )
        value.append( price_inclu_tax )
        stock = data_value[5].text
        stock = [i for i in stock if i.isdigit()]
        stock = "".join( stock )
        value.append( stock )
        data_description = s.find_all( 'p' )

        data_description = data_description[3].text
        value.append( data_description )

        data_cat = s.find_all( 'a' )
        data_cat = data_cat[3]
        data_cat = data_cat.string
        logging.info( f"data_cat : {data_cat}" )
        value.append( data_cat )

        rating = s.find( 'p', {'class': re.compile( r'star-rating.*' )} )
        rating = rating["class"]

        value.append( rating[1] )

        data_image_url = s.find_all( 'img' )
        data_image_url = data_image_url[0].get( "src" )

        value.append( "http://books.toscrape.com/" + data_image_url )

        return csv_header, value


    def loading(a, b):  # a, data_book
        """write on the csv file

        Args:
            a(list(str)):table header
            b:data from books

        Returns:
            csv files with datas from books

        """

        with open( b[7] + ".csv", "a", newline="", encoding="utf-8" ) as csv_file:
            writer = csv.writer( csv_file, delimiter="," )
            file_is_empty = os.stat( b[7] + ".csv" ).st_size == 0
            if file_is_empty:
                writer.writerow( a )
            writer.writerow( b )


    # noinspection PyShadowingNames
    def get_pictures(data_book):
        """dowload book pictures and creating of data folder, categorie folder and book folder

        Args:
            data_book(list(str)): data from books

        """
        link = data_book[9].replace( "../../", "" )
        title = data_book[2]
        title = "".join( [i for i in title] )
        cat = data_book[7]
        urllib.request.urlretrieve( link, title )
        img = Image.open( title )
        img.save( title + ".png" )

        try:
            base_dir = Path.cwd()

            files_png = [f for f in base_dir.iterdir() if f.is_file() and f.suffix == ".png"]

            for f in files_png:
                output_dir = base_dir / "DATA" / cat / title
                output_dir.mkdir( exist_ok=True, parents=True )

                f.rename( output_dir / f.name )

            [f.unlink() for f in base_dir.iterdir() if f.is_file() and f.suffix == ""]
        except FileExistsError:
            logging.info( "Files already created" )

        except FileNotFoundError:
            logging.info( "path no found" )


    soup = extract( url_books[url] )
    header, line_1 = transform( soup, url_books[url] )
    loading( header, line_1 )  # a, data_book
    get_pictures( line_1 )

# creates a folder for the .csv files and stores them in it
try:
    BASE_DIR = Path.cwd()
    filepath = Path( BASE_DIR / "DATA" )
    filepath.mkdir( exist_ok=True )

    files = [f for f in BASE_DIR.iterdir() if f.is_file() and f.suffix == ".csv"]

    for file in files:
        starget_file = file.stem

        logging.info( f"Files name:{file.stem}" )
        absolut_starget_folder = filepath / starget_file
        absolut_starget_folder.mkdir( exist_ok=True )
        file_cible = absolut_starget_folder / file.name

        file.rename( file_cible )

except FileExistsError:
    logging.debug( "Files already created" )
