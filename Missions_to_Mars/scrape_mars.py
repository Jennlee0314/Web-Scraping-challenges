#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import re
import pandas as pd


# NASA Mars News
def scrape_info():
        
    browser = Browser('chrome')


    mars = {}


    url = "https://mars.nasa.gov/news"
    browser.visit(url)


    soup = bs(browser.html, 'html.parser')



    result = soup.find_all('div', class_="content_title")[1]

    news_title = result.a.text


    result1 = soup.find('div', class_="article_teaser_body").text



    result1


    news_p = result1



    mars["news_title"] = news_title
    mars["news_p"] = news_p


    #  JPL Mars Space Images - Featured Image

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)


    full_image_element = browser.find_by_id('full_image')
    full_image_element.click()



    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_element =  browser.find_link_by_partial_text('more info')
    more_info_element.click()



    html = browser.html
    img_soup = bs(html,'html.parser')



    img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    img_url_rel


    image_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    image_url
    mars['featured_image_url']=image_url


    browser = Browser('chrome')

    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)

    html_weather = browser.html

    weather_soup = bs(html_weather, 'html.parser')


    mars_weather = weather_soup.find_all(string = re.compile('low.*high.*'))[0]
    mars_weather
    mars['mars_weather'] = mars_weather


    # Mars Facts


    marsfacts_url = "https://space-facts.com/mars/"
    browser.visit(marsfacts_url)


    marsfacts_soup = bs(browser.html, 'html.parser')

    marsfacts_result = marsfacts_soup.find_all('table', id="tablepress-p-mars")[0]
    marsfacts_result


    marsfacts_df = pd.read_html(marsfacts_url)[0]


    marsfacts_df.columns = ['description', 'value']
    marsfacts_df.set_index('description', inplace = True)
    marsfacts_df



    mars["facts"] = marsfacts_df.to_html()


    browser = Browser('chrome')


    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)



    hemispheres_images_url = []

    full_resolution_images = browser.find_by_css('a.product-item h3')
    print(full_resolution_images)

    for i in range(len(full_resolution_images)):
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.find_link_by_text('Sample').first
        hemispheres["img_url"] = element['href']
        hemispheres['titles'] = browser.find_by_css('h2.title').text
        hemispheres_images_url.append(hemispheres)
        browser.back()
    hemispheres_images_url   
        



    mars['hemisphere'] = hemispheres_images_url 


    return mars

    

if __name__ == "__main__":
    print(scrape_info())