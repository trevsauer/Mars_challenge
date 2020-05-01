from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd

def scrape():
    # URLs of pages to be scraped
    mars_nasa = 'https://mars.nasa.gov/news/'
    mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_weather = 'https://twitter.com/marswxreport?lang=en'
    mars_facts = 'http://space-facts.com/mars/'
    mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    response_mars_nasa = requests.get(mars_nasa)
    soup = BeautifulSoup(response_mars_nasa.text, 'html.parser')
    results = soup.find_all(class_="slide")
    list_titles = []
    list_pp = []

    for result in results:
            links = result.find_all('a')
            title = links[1].text
            paragraph = result.find(class_="rollover_description_inner").text
            list_titles.append(title)
            list_pp.append(paragraph)
    news_title = list_titles[0]
    news_p = list_pp[0]


    response_image = requests.get(mars_image)
    soup = BeautifulSoup(response_image.text, 'html.parser')
    results = soup.find_all(class_="carousel_items")

    for result in results:
        article = result.find('article', class_="carousel_item")
        link_article = article['style']
        cleaned_link_article = article['style'].lstrip('background-image: url(')
        cleaned_link_article = cleaned_link_article.rstrip(');')
    cleaned_link_article = cleaned_link_article.replace("'", "")
    feat_image_link = 'https://www.jpl.nasa.gov'+cleaned_link_article


    response_weather = requests.get(mars_weather)
    soup = BeautifulSoup(response_weather.text, 'html.parser')
    results = soup.find_all(class_="content")
    list_tweets = []
    for result in results:
        tweet = result.find('p', class_="TweetTextSize").text
        list_tweets.append(tweet)
    mars_weather = list_tweets[0]

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    usgs_base = 'https://astrogeology.usgs.gov'
    list_links = []
    hemispheres_response = requests.get(mars_hemispheres_url)
    soup = BeautifulSoup(hemispheres_response.text, 'html.parser')

    results = soup.find_all(class_='item')
    for result in results:
        links = result.find('a')
        link=links['href']
        list_links.append(usgs_base+link)
        browser.visit(mars_hemispheres)

    hemispheres_image = []
    list_titles = []

    for x in range(0, 4):
        browser.visit(list_links[x])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find(class_='downloads')
        image = images.find('a')
        image_url= image['href']
        hemispheres_image.append(image_url)
        titles = soup.find('h2', class_='title')
        title=titles.text
        title=title.strip('Enhanced')
        list_titles.append(title)

    hemispheres_dict = {'Title': list_titles,
                        'URL': hemispheres_image }
    scraped_dict = {'Title': list_titles,
                    'URL': hemispheres_image,
                    'Weather': mars_weather,
                    'Featured Image': feat_image_link,
                    'News Title': news_title,
                    'News Body': news_p
               }
    return (scraped_dict)