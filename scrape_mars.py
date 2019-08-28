#Import dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from splinter import Browser
import sys
import json
from flask import Flask, render_template


def scrape():
    #Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
    #data = {}
    #Nasa news
    #URL to be scrapped
    url = "https://mars.nasa.gov/news/"

    #Retrive page with the request module
    response = requests.get(url)

    #Create a BeautifulSoup object
    soup_nasa = BeautifulSoup(response.text, 'html')
    #soup_nasa

    #Retrieve title and paragraph
    nasa_title = soup_nasa.find('div', class_="content_title").text
    nasa_text = soup_nasa.find('div', class_='rollover_description_inner').text

    #Clean data
    nasa_title = nasa_title.replace('\n', '')
    nasa_text = nasa_text.replace('\n', '')

    #JPL image
    #URL to be scrapped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.find_by_css('a.button').click()
    jpl_soup = BeautifulSoup(browser.html, 'html.parser')
    #jpl_soup

    #Retrieve image url
    image = jpl_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image
    featured_image_url

    #URL to be scrapped
    twitter_url = "https://twitter.com/marswxreport?lang=en"

    #Retrive page with the request module
    response = requests.get(twitter_url)

    #Create a BeautifulSoup object
    soup_twitter = BeautifulSoup(response.text, 'html')
    #soup_twitter

    #Retreive latest tweet
    mars_weather = soup_twitter.find(
        'div', class_="js-tweet-text-container").text
    mars_weather = mars_weather.replace('\n', '')
    #extra = 'pic.twitter.com/MhPPOHJg3m'
    #mars_weather = mars_weather.split(extra, 1)[0]
    mars_weather

    #Mars Facts
    #URL to be scrapped
    facts_url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(facts_url)
    #tables

    # Create DataFrame
    df = tables[0]
    df.columns = ['Concept', 'Mars', 'Earth']
    df = df.drop(columns=["Earth"])
    df

    #Build html table
    tables = df.to_html()
    #table

    #Mars Hemispheres
    #URL to be scrapped
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    hemis_soup = BeautifulSoup(browser.html, 'html.parser')
    #hemis_soup

    #Find headers
    headers = []
    titles = hemis_soup.find_all('h3')
    titles

    #Clean headers
    for title in titles:
        headers.append(title.text)
    print(headers[0:3])

    #Images
    one = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    two = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    three = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    four = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    images = [one, two, three, four]
    images

    #Append list
    hemisphere_image_urls = [{'title': headers, 'img_url': images}
                             for headers, images in zip(headers, images)]
    hemisphere_image_urls

    data = {
        'Nasa_news': nasa_title,
        'Nasa_text': nasa_text,
        'Nasa_image': featured_image_url,
        'Mars_weather': mars_weather,
        'Mars_facts': tables,
        'Hemisphere': hemisphere_image_urls
    }

    browser.quit()

    return data
