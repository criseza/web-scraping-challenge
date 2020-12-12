# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

# Create Browser using splinter
def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

### NASA Mars News

## Create a dictionary for scraped data
scrape = {}

# URL for scraping
browser = init_browser()
news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)

# Scrape into Soup
news_html = browser.html
news_soup = bs(news_html, 'html.parser')

# Check contents
# print(soup.prettify())

# Get News Title
article = news_soup.find('div', class_='list_text')
news_title = article.find('div', class_='content_title').text
news_title

# Get Paragraph Text
news_p = news_soup.find("div", class_="article_teaser_body").text.strip('\n')
news_p

## Add scraped data to the dictionary
scrape['news_title'] = news_title
scrape['news_p'] = news_p

### JPL Mars Space Images - Featured Image

# URL for scraping
browser = init_browser()
img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(img_url)

# Scrape into Soup
img_html = browser.html
img_soup = bs(img_html, 'html.parser')

base = 'https://jpl.nasa.gov'
image = img_soup.find("article", class_="carousel_item")["style"]
featured_image_url = base + image
featured_image_url

## Add scraped image url to the dictionary
scrape["featured_image_url"] = featured_image_url

### Mars Weather (NOT ACTIVE)

### Mars Facts

# URL for scraping
browser = init_browser()
facts_url = 'https://space-facts.com/mars/'
browser.visit(facts_url)

# Scrape into Soup
facts_html = browser.html
facts_soup = bs(facts_html, 'html.parser')

# Make the table
mars_facts_table = pd.read_html(facts_url)
mars_facts_df = mars_facts_table[0]
mars_facts_df.columns = ['Description','Value']
mars_facts = mars_facts_df.set_index('Description',inplace=True)
print(mars_facts_df)

## Add facts HTML to the dictionary
mars_facts_html = mars_facts_df.to_html()
scrape['facts'] = mars_facts_html

### Mars Hemispheres

# URL for scraping
browser = init_browser()
hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hem_url)

# Scrape into Soup
hem_html = browser.html
hem_soup = bs(hem_html, 'html.parser')

# Images URLs
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
]

## Add hemisphere images URLs to the dictionary
scrape['hem_img'] = hemisphere_image_urls

browser.quit()

# Print complete dictionary to insert to mongo
scrape