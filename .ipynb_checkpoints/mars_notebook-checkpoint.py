# dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd

# url pages to be scraped and used 
mars_nasa = 'https://mars.nasa.gov/news/'
mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
mars_weather = 'https://twitter.com/marswxreport?lang=en'
mars_facts = 'http://space-facts.com/mars/'
mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# use requests module to get information from mars_nasa
response_mars_nasa = requests.get(mars_nasa)
# use beautiful soup, create object and parse with html.parser
soup = BeautifulSoup(response_mars_nasa.text, 'html.parser')
# display content to show what there is to scrape
print(soup.prettify())

# results are returned as an iterable list
results = soup.find_all(class_="slide")
list_titles = []
list_pp = []
# loop through all the returned results 
for result in results:
    # handling errors
    try:
        #find the title and pp for each of the links. the title is found in the second link of each slide, while pp is inside the div tag description
        links = result.find_all('a')
        title = links[1].text
        paragraph = result.find(class_="rollover_description_inner").text
        # append each variable to predetermined lists
        list_titles.append(title)
        list_pp.append(paragraph)
        
        print(title)
        print(paragraph)
    except AttributeError as e:
        print(e)

# store the first title and body 
first_title = list_titles[0]
first_pp = list_pp[0]
print(first_title)
print(first_pp)

# scrape for mars image and retreive page with requests module
image_pull = requests.get(mars_image)
# use beautiful soup, create object and parse with html.parser
soup = BeautifulSoup(image_pull.text, 'html.parser')
print(soup.prettify())

# return results as iterable list
results = soup.find_all(class_="carousel_items")
# loop through results 
for result in results:
    # handle erroes
    try:
        #query article tag and distinguish it as a 'style' parameter 
        article = result.find('article', class_="carousel_item")
        link_article = article['style']
        #Use modification to fix the link to be in the correct format
        cleaned_link_article = article['style'].lstrip('background-image: url(')
        cleaned_link_article = cleaned_link_article.rstrip(');')
        # show the link, the link once cleaned, and the article it was taken from 
        print(link_article)
        print(cleaned_link_article)
        print(article)
    except AttributeError as e:
        print(e)

# remove quotes from beginning and end of the string and then create the url for the image 
cleaned_link_article = cleaned_link_article.replace("'", "")
featured_image_link = 'https://www.jpl.nasa.gov'+cleaned_link_article
print(featured_image_link)

# get the page with the requests module 
weather_response = requests.get(mars_weather)
# create B soup object and parse with html.parser
soup = BeautifulSoup(weather_response.text, 'html.parser')
# look at the results
print(soup.prettify())

# results are returned as an iterable list
results = soup.find_all(class_="content")
list_tweets = []
# loop through the returned results 
for result in results:
    # handle errors
    try:
        # find the test of the tweets and append it to the tweet text 
        tweet = result.find('p', class_="TweetTextSize").text
        list_tweets.append(tweet)
    except AttributeError as e:
        print(e)

#  store the most recent tweets as first tweets that are added to the list and you can always modify the index to return the first weather entry as a way to check the recent updates 
mars_weather = list_tweets[0]

# use pandas to scrape the data 
table_of_facts = pd.read_html(mars_facts)
table_of_facts

# make a new dataframe that pulls the information from table of tacts and turns it into a dictionary 
keys = list(table_of_facts[0][0])
values = list(table_of_facts[0][1])
facts_dict = dict((keys[x],values[x]) for x in range(0,len(keys)))

# drop the columns that are not needed and show the respective df 
facts_df = pd.DataFrame(facts_dict, index=[0])
facts_df = facts_df.drop(['First Record:', 'Recorded By:'], axis=1)
facts_df

# rename the columns
cols = facts_df.columns.tolist()

new_columns = ['Equatorial Diameter:', 'Polar Diameter:', 'Mass:', 'Orbit Distance:', 'Orbit Period:', 'Surface Temperature:', 'Moons:']
facts_df = facts_df[new_columns]
facts_df

# setup the Chrome Driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# create the base url and the lists that hold all the necessary links 
usgs_base= 'https://astrogeology.usgs.gov'
links_list = []
hemispheres_response = requests.get(mars_hemispheres)
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(hemispheres_response.text, 'html.parser')

results = soup.find_all(class_='item')
# loop through all the results 
for result in results:
    # handle the errors 
    try:
        # find the tag which will link you to a speciic page 
        links = result.find('a')
        # return the link and print it 
        link=links['href']
        print(link)
       
        # add in the usgs url to complete the full url and add that to a list of the finished links 
        links_list.append(usgs_base+link)
    except AttributeError as e:
        
print(links_list)

# use spliinter to tap into the hemispheres url 
browser.visit(mars_hemispheres)

# create the lists that hold all of the urls and their respective titles 
hemispheres_image = []
first_title = []

for x in range(0, 4):
    # navigate through all the four page links 
    browser.visit(links_list[x])

    # print each of the links as they are being processed 
    print(links_list[x])

    # create soup object 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # look for the jpg that we want in the downloads class 
    images = soup.find(class_='downloads')

    # search for the link tag which then retrieves the desired link 
    image = images.find('a')
    image_url= image['href']

    # append that to the hemispheres_image list
    hemispheres_image.append(image_url)

    # searcg for the title and append that to the list of titles 
    titles = soup.find('h2', class_='title')
    title=titles.text
    title=title.strip('Enhanced')
    titles_list.append(title)

# create a dictionary for hemisheres that holds the title and the url 
hemispheres_dict = {'Title': titles_list,
                    'URL': hemispheres_image }

                    # create a dictionary with all the scraped data
scraped_dict = {'Title': titles_list,
                'URL': hemispheres_image,git init
                'Weather': mars_weather,
                'Featured Image': featured_image_link,
                'News Title': first_title,
                'News Body': news_p
               }
