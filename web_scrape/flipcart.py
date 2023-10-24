import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class": 'B_NuCI'})
        # Inner NavigatableString Object
        title_value = title.text
        # Title as a string value
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("div", attrs={'class': '_30jeq3 _16Jk6d'}).string.strip()
    except AttributeError:
        price = 0
    return price


def get_price_original(soup):
    try:
        price = soup.find("div", attrs={'class': '_3I9_wc _2p6lqe'}).text
    except AttributeError:
        price = ""
    return price


def get_price_off(soup):
    try:
        price = soup.find("div", attrs={'class': '_3Ay6Sb _31Dcoz'}).string.strip().split("%")[0]
    except AttributeError:
        price = 0

    return price


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("div", attrs={'class': '_3LWZlK'}).text
    except AttributeError:
        rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'class': '_2_R_DZ'}).text.split("&")[1]
    except AttributeError:
        review_count = ""
    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'class': '_2JC05C'}).text
    except AttributeError:
        available = "Not Available"

    return available


if __name__ == '__main__':

    # add your user agent
    HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.flipkart.com/search?q=badminton&as-searchtext=badminton"
    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'target': '_blank'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    d = {"title": [], "price": [], "originalPrice": [], "off %": [], "rating": [], "reviews": [], "availability": [],
         "link": []}

    count = 0
    # Loop for extracting product details from each link
    for link in links_list:
        # fetching for 10 products only
        if count >= 10:
            continue

        new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['originalPrice'].append(get_price_original(new_soup))
        d['off %'].append(get_price_off(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))
        # d['link'].append("https://www.flipkart.com" + link)
        count = count + 1
        print(count)

    flipkart_df = pd.DataFrame.from_dict(d)
    flipkart_df = flipkart_df.sort_values(by=['off %'], ascending=True)
    flipkart_df['title'].replace('', np.nan, inplace=True)
    flipkart_df = flipkart_df.dropna(subset=['title'])
    flipkart_df.to_csv("flipkart.csv", header=True, index=False)
