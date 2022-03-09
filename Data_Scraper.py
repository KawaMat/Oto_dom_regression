import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import time


# Scraper


# Page
page = 1
# Link with flats which we want to scrape
link_base = r'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?distanceRadius=5&limit=72&page='
# Create a full link (first page)
link = link_base + str(page)
# Create a dataframe (store data)
df = pd.DataFrame()



# Make a request
r = requests.get(link)
# Create a soup object
soup = bs(r.content, features="html.parser")



# Count number of an advertisements
adds_no = int(soup.find_all('span', {'class': 'css-klxieh e1ia8j2v11'})[0].get_text())



# Adds per page
adds_per_page = 72
# Calculate number of pages
pages = int(np.ceil(adds_no / adds_per_page))

# Full scraper



# pages = 2



# Get data from pages (1: number of pages)
for page in range(2, (pages + 1)):

    try:

        # Articles (not promoted - [1])
        not_promoted = soup.find_all('ul', {'class': 'css-14cy79a e3x1uf06'})[1]
        articles = soup.find_all('ul', {'class': 'css-14cy79a e3x1uf06'})[1].select('article')
        # Offer links
        hrefs = []
        # Iterate through not promoted to get an offer href
        for offer in not_promoted:
            try:
                # Get href and create a full link
                href = offer.find_all('a', {'class': 'css-1c4ocg7 es62z2j23'})[0]['href']
                href = 'https://www.otodom.pl' + href
                hrefs.append(href)
            except:
                pass

        # Lists for data and column names storing
        col_names_to_add = ['Tytul', 'Cena', 'Lokalizacja', 'URL']
        column_names = []
        data_to_add = []
        data_csv = []

        # Iterate through articles (advertisements urls)
        for article_no, article_href in enumerate(hrefs):

            try:
                print("Page: " + str(page - 1) + '/' + str(pages) + ', add: ' + str(article_no + 1) + '/' + str(
                    len(hrefs)))

                # Get new offer content (article_href)
                time.sleep(0.3)
                # Make a request
                r_offer = requests.get(article_href)
                # Create a soup object
                soup_offer = bs(r_offer.content, features="html.parser")

                # Offer title
                offer_title = articles[article_no].find_all("h3", {"class": "css-1rhznz4 es62z2j20"})[0]['title']
                # Price

                item_price = articles[article_no].find_all("p", {"class": "css-1bq5zfe es62z2j16"})[
                                 0].get_text().replace(
                    "\xa0", "")[:-2]

                # Localization
                localization = articles[article_no].p.span.get_text()

                # Add data to list (always available)
                data_to_add.extend([offer_title, item_price, localization, article_href])


                parameters = soup_offer.find_all("div", {'class': 'css-wj4wb2 emxfhao1'})[0].find_all("div", {"class",
                                                                                                              "css-1ccovha estckra9"})

                # parameters[0].select('div')[1].get_text()
                # parameters[0].select('div')[2].get_text()

                # Get parameters
                col_names = []
                data = []

                for param in parameters:
                    col_names.append(param.select('div')[1].get_text())
                    data.append(param.select('div')[2].get_text())

                # If additional info exists
                add_params = soup_offer.find_all("div", {'class': 'css-1l1r91c emxfhao1'})

                # If add_params available
                if (add_params):
                    add_params = add_params[0].find_all("div", {"class", "css-f45csg estckra9"})

                    for param in add_params:
                        col_names.append(param.select('div')[1].get_text())
                        data.append(param.select('div')[2].get_text())

                #### /MY

                # Add lists content to single advertisement lists
                col_names_to_add.extend(col_names)
                data_to_add.extend(data)

                # Add to lists (DataFrame)
                column_names.append(col_names_to_add)
                data_csv.append(data_to_add)

                # Clear lists for current advertisement
                col_names_to_add = ['Tytul', 'Cena', 'Lokalizacja', 'URL']
                data_to_add = []

            except:
                # Error message
                print("Error! Page: " + str(page - 1))

                # Clear lists for current advertisement
                col_names_to_add = ['Tytul', 'Cena', 'Lokalizacja', 'URL']
                data_to_add = []

        # DataFrame update (row by row)
        for element in range(len(data_csv)):
            df = df.append(pd.DataFrame([data_csv[element]], columns=column_names[element]), sort=False)

    except:
        print('Error on page: ' + str(page))

    # URL update
    link = link_base + str(page)
    print("Next page will be: " + link)

    # Make a request to next page
    r = requests.get(link)
    # Create a soup object
    soup = bs(r.content, features="html.parser")

# Save data to csv file
filepath = f'data_scraping.csv'
df.to_csv(filepath, sep=';', index=False, encoding='utf-8-sig')