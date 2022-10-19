import csv
import re
import string
import urllib.request
from pathlib import Path

import requests
from PIL import Image
from bs4 import BeautifulSoup

from url import url_books

for url in range( 5 ):  # len(url_books)

    def extract(url_books):
        """scrape the page web of books

        Args:
            url_books(str):

        Returns:
            scraped web page

        """
        r = requests.get( url_books )
        if r.status_code != 200:
            print( "problème d'url" )

        soup = BeautifulSoup( r.content, 'html.parser' )

        return soup

    def transform(soup, url):
        """get datas for books (product_page_url", "universal_product_code (upc)", "title", "price_including_tax",
                  "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                  "image_url)
        Args:
            soup(soup):scraped web page
            url(str):url of a book

        Returns:
            all datas for books

        """
        value = [url]
        header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax",
                  "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                  "image_url"]

        h1 = soup.find( "h1" ).text
        data_value = soup.find_all( 'td' )
        for i in range( 6 ):
            value.append( data_value[i].text )
            if i == 0:
                value.append( h1 )
            else:
                pass
        if "Books" or "£0.00" in value:
            value.remove( "Books" )
            value.remove( "£0.00" )

        data_description = soup.find_all( 'p' )
        data_description = data_description[3].text
        value.append( data_description )

        data_cat = soup.find_all( 'a' )
        data_cat = data_cat[3]
        data_cat = data_cat.string

        value.append( data_cat )

        a = soup.find( 'p', {'class': re.compile( r'star-rating.*' )} )
        a = a["class"]

        value.append( a[1] )

        data_image_url = soup.find_all( 'img' )
        data_image_url = data_image_url[0].get( "src" )

        value.append( "http://books.toscrape.com/" + data_image_url )

        return header, value


    def loading(header, line_1):  # header, line_1
        """write on the csv file

        Args:
            header(list(str)):table header
            line_1:data from books

        Returns:
            csv files with datas from books

        """

        with open( line_1[7] + ".csv", "a", newline="", encoding="utf-8" ) as csv_file:
            writer = csv.writer( csv_file, delimiter="," )
            if url == 0:
                writer.writerow( header )
            else:
                pass
            writer.writerow( line_1 )


    def get_pictures(line_1):
        """dowload book pictures and creating of data folder, categorie folder and book folder

        Args:
            line_1(list(str)): data from books

        """

        link = line_1[9].replace( "../../", "" )
        print( link )
        title = line_1[2]
        title = "".join( [i.rstrip() for i in title if i not in string.punctuation] )
        print( title )
        cat = line_1[7]
        print( cat )
        list_zip = (title, cat)
        print( list_zip )
        urllib.request.urlretrieve( link, title )
        img = Image.open( title )
        img = img.save( title + ".png" )

        try:
            BASE_DIR = Path.cwd()

            files = [f for f in BASE_DIR.iterdir() if f.is_file() and f.suffix == ".png"]

            for f in files:
                output_dir = BASE_DIR / "DATA" / cat / title
                output_dir.mkdir( exist_ok=True, parents=True )

                f.rename( output_dir / f.name )

            a = [f.unlink() for f in BASE_DIR.iterdir() if f.is_file() and f.suffix == ""]
        except FileExistsError:
            print( "Files already created" )
            pass
        except FileNotFoundError:
            print( "path no found" )
            pass


    soup = extract( url_books[url] )
    header, line_1 = transform( soup, url_books[url] )
    loading( header, line_1 )  # header, line_1
    get_pictures( line_1 )

# creates a folder for the .csv files and stores them in it
try:
    BASE_DIR = Path.cwd()
    filepath = Path( BASE_DIR / "DATA" )
    filepath.mkdir( exist_ok=True )

    files = [f for f in BASE_DIR.iterdir() if f.is_file() and f.suffix == ".csv"]

    for file in files:
        starget_file = file.stem
        print( type( file.stem ) )
        print( file.stem )
        absolut_starget_folder = filepath / starget_file
        absolut_starget_folder.mkdir( exist_ok=True )
        file_cible = absolut_starget_folder / file.name
        # print( file_cible )

        file.rename( file_cible )

except FileExistsError:
    print( "Files already created" )
    pass
