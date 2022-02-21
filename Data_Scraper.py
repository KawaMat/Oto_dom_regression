#package import
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

# Scraper
#Link with flats that we want scrape
link_base = r'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?distanceRadius=5&page='
#create a full link (first page)
link= link_base + '1'

#Create a dataframe (store data)
df = pd.DataFrame()

#Make a request

r = requests.get(link)
#Create a soup object
soup = bs(r.content, features='html.parser')

# count number of advertisements
adds_no = int(soup.find_all('span',{'class':'css-klxieh e1ia8j2v11'})[0].get_text())


#Adds per page
adds_per_page = 72
#Calculate number of pages
pages = int(np.ceil(adds_no/adds_per_page))
#print(pages)
not_promoted = soup.find_all('ul', {"class": 'css-14cy79a e3x1uf06'})[1]
articles = soup.find_all('ul', {"class": 'css-14cy79a e3x1uf06'})[1].select('article') #[1]  to exlude promoted positions

#offers links

hrefs = []
#Iterate over not promoted to get an offer href
for offer in not_promoted:
    try:
        #get page ref and create full link
        href = offer.find_all('a',{'class':'css-jf4j3r es62z2j27'})[0]["href"]
        href = 'http://www.otodom.pl'+href
        hrefs.append(href)
        print(href)
    except:
        print('Error')
