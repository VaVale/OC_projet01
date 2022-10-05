import csv
from pprint import pprint

import url

import requests
from bs4 import BeautifulSoup
import pandas

url = url.url


for i in range(len(url)):

    print(i)
    def extract(url):
        print(url)
        r = requests.get(url)
        if r.status_code != 200:
            print("problème d'url")
        # print(r.status_code)

        soup = BeautifulSoup( r.content, 'html.parser' )

        return soup


    def transform(soup):
        key = []
        value = []

        data_value= soup.find_all('td')
        for i in range(6):
            value.append(data_value[i].text)

        data_key = soup.find_all('th')

        for i in range(6):
            key.append(data_key[i].text)

        h1 = soup.find("h1").text
        value.append(h1)
        key.append("Title")
        # print(key)
        # print( value )

        data_rating = soup.find('p' ,{"class":"star-rating Two"})
        data_rating = data_rating["class"]

        key.append(data_rating[0])
        value.append(data_rating[1])

        # return data
        data_cat = soup.find_all( 'a' )
        data_cat = data_cat[3]
        data_cat = data_cat.string
        key.append("categories")
        value.append(data_cat)


        data_image_url = soup.find_all('img')
        data_image_url = data_image_url[0].get("src")
        key.append("image_url")
        value.append("http://books.toscrape.com/"+data_image_url)

        data_description = soup.find_all('p')
        data_description = data_description[3].text

        key.append(soup.h2.text)
        value.append(data_description)
        print(key)
        print(value)
        return key, value

    def loading(line_1, line_2):
        with open( "test.csv", "w", newline="" ) as csv_file:
            writer = csv.writer( csv_file, delimiter="," )
            writer.writerow( line_1 )
            writer.writerow( line_2 )

    soup = extract( url[i] )
    #
    line_1,line_2 = transform( soup )
    loading(line_1,line_2)



