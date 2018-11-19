
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, wait_time=60, fullscreen=False, incognito=True, headless=False)


def scrape():
    # Dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import requests
    import pymongo
    import pandas as pd
    import time

    #chromebrowser set up
    executable_path = {"executable_path": "chromedriver"}
    browser =  Browser("chrome", **executable_path, headless=False)

    #URL's to scrape
    url1 = 'https://mars.nasa.gov/news/'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url3 = 'https://twitter.com/marswxreport?lang=en'
    url4 = 'http://space-facts.com/mars/'
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # **************************************************************************
    # NASA Mars News
    # Scrape https://mars.nasa.gov/news/ and get the latest news title and text
    # **************************************************************************

    #Nasa Mars News
    browser.visit(url1)

    # Retrieve page with the requests module
    response = browser.html
    soup = bs(response, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)


    # **************************************************************************
    # JPL Mars Space Images - Featured Image
    # Scrape https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars and get the link for the larget carousel image
    # **************************************************************************

    # Access full image from JPL Mars Space Images
    browser.visit(url2)
    f1 = browser.find_by_id("full_image")
    
    f1.click()

    time.sleep(1)

    browser.click_link_by_partial_text('more info')

    # Retrieve page with the requests module
    response2 = browser.html
    soup2 = bs(response2, 'html.parser')

    #main_url = main one for in front
    main_url = 'https://www.jpl.nasa.gov'
    page_url = soup2.find(class_='lede').find('a').get('href')
    featured_image_url = main_url + page_url
    print(featured_image_url)

    # **************************************************************************
    # Mars Weather
    # Scrape https://twitter.com/marswxreport?lang=en and get and save the westher tweets
    # **************************************************************************

    # Retrieve page with the requests module to get Mars Weather
    response3 = requests.get(url3)
    soup3 = bs(response3.text, 'html.parser')

    mars_weather_find = soup3.find_all('div', class_='js-tweet-text-container')
    mars_weather = (mars_weather_find[0].p.text)

    # **************************************************************************
    # Mars Facts
    # Scrape https://space-facts.com/mars/ and get and save the facts to an HTML table string 
    # 
    # **************************************************************************

    #Get Mars Facts
    tables = pd.read_html(url4)[0]
    tables.columns = ('fact', 'figure')
    tables.set_index('fact', inplace=True)
    tables

    #Put Mars facts in HTML table string
    table_string = tables.to_html()
    print(table_string)


    # **************************************************************************
    # Mars Hemispheres
    # Scrape https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars and 
    # get and save the high resolution images for each of Mars hemispheres
    # **************************************************************************

    # Visit and get Mars Hemispheres information - URL and title of each Hemisphere
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemisphere_image_urls = []

    # Store the main_ul
    main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items:
        # Store title
        title = i.find('h3').text.strip('Enhanced')

        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']

        # Visit the link that contains the full image website
        browser.visit(main_url + partial_img_url)

        # HTML Object
        partial_img_html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs( partial_img_html, 'html.parser')

        # Retrieve full image source
        img_url = main_url + soup.find('img', class_='wide-image')['src']

        # Append to dictionaries
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # Create dictionary
    mars = []
    mars.append({"news_title" : news_title, "news_short" : news_p, "featured_image_url" : featured_image_url,
            "mars_weather" : mars_weather, "mars_facts" : table_string, "hemispheres_urls" : hemisphere_image_urls})
    # return data
    return mars

