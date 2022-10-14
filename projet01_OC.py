import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from url import url_books

start = time.time()

for i in range( len( url_books ) ):  # len(url_books)

    def extract(url_books):
        # print(url)
        r = requests.get( url_books )
        if r.status_code != 200:
            print( "problème d'url" )
        # print(r.status_code)

        soup = BeautifulSoup( r.content, 'html.parser' )

        return soup


    def transform(soup, url):

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

        return header, value, data_cat


    def loading(header, line_1):  # header, line_1
        # file_path = Path(Path.cwd() / line_1[7]+".csv")
        # file_path.parent.mkdir(parents=True, exist_ok=True)

        with open( line_1[7] + ".csv", "a", newline="", encoding="utf-8" ) as csv_file:
            writer = csv.writer( csv_file, delimiter="," )
            if i == 0:
                writer.writerow( header )
            else:
                pass
            writer.writerow( line_1 )


    soup = extract( url_books[i] )
    header, line_1, dat_cat = transform( soup, url_books[i] )
    loading( header, line_1 )  # header, line_1

try:
    BASE_DIR = Path.cwd()
    filepath = Path( BASE_DIR / "DATA" )
    filepath.mkdir( exist_ok=True )

    files = [f for f in BASE_DIR.iterdir() if f.is_file() and f.suffix == ".csv"]

    for file in files:
        starget_file = file.stem

        absolut_starget_folder = filepath / starget_file
        absolut_starget_folder.mkdir( exist_ok=True )
        file_cible = absolut_starget_folder / file.name
        print( file_cible )

        file.rename( file_cible )

except FileExistsError:
    print( "Files already exist" )

    # BASE_DIR  = Path.cwd()
    # files = [f for f in BASE_DIR.iterdir() if f.is_file()]
    # print(files)
    # for file in files:
    #     absolute_target_folder = BASE_DIR / line_1[2]
    #     absolute_target_folder.mkdir(exist_ok=True)
    #     file_cible = absolute_target_folder / line_1[7]+".csv"
    #     file.rename(file_cible)

    # df = pd.read_csv("all_books.csv")

end = time.time()
elapsed = end - start

print( f"temps d'execution = : {elapsed}ms")
