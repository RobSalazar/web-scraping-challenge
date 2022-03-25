#!/usr/bin/env python
# coding: utf-8

# ## Mission to Mars


#Import modules
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager

#Initializing browser and setting its path
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)




# Start by converting your Jupyter notebook into a Python script called 
# scrape_mars.py with a function called scrape that will execute all of your
# scraping code from above and return one Python dictionary containing all of the scraped data.  
def scrape():
    
    # ## NASA Mars News

    browser = init_browser()
    
    #Navigate to url for scraping
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    #Get browser html into object for scraping
    nasa_html = browser.html

    #Parse with beautiful soup parser
    soup = bs(nasa_html, "html.parser")

    #Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    #Assign the text to variables that you can reference later.
    results = soup.find('div' , class_ = "list_text")

    news_title = results.a.text
    news_p = results.find("div" , class_ = "article_teaser_body").text
    print(news_title)
    print(news_p)


    # ## JPL Mars Space Images - Featured Image


    #Navigate to url for scraping
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
    time.sleep(1)

    #Get browser html into object for scraping
    jpl_html = browser.html

    #Parse with beautiful soup parser
    soup = bs(jpl_html, "html.parser")

    #Find the correct class and source for the image
    img = soup.find('img', class_="headerimage fade-in")
    featured_img = jpl_url+img["src"]
    print(featured_img)


    # ## Mars Facts


    #Navigate to url for scraping
    mars_url = 'https://space-facts.com/mars/'
    browser.visit(mars_url)
    time.sleep(1)

    #Read html with pandas to create a df
    mars = pd.read_html(mars_url)

    #Convert to df and rename the columns, then for formatting remove index to keep end result clean
    df = mars[0]
    df.columns = ["Description" , "Value"]
    df.to_html("marstable.html",index = False)
    
    

    # ## Mars Hemispheres


    #Navigate to url for scraping
    base_url  = "https://marshemispheres.com/"
    browser.visit(base_url)

    #Container to hold  our loop iterations
    all_urls = []

    #Iterate through the 4 different links to get the images needed
    for x in range(4):
        html = browser.html
        soup = bs(html, "html.parser")
        
        title = soup.find_all("h3")[x].get_text()
        browser.find_by_tag("h3")[x].click()
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        img_url = soup.find("img", class_="wide-image")["src"]
        all_urls.append({
            "title":title,
            "img_url": base_url+img_url
        })
        browser.back()
    browser.quit()
        
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        'featured_img': featured_img,
        # "df": df,
        "all_urls": all_urls
    }
    
    return mars_data