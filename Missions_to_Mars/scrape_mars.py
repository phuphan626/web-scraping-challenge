#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from config import chrome_driver_path as cdp
import time


# In[2]:

def init_browser():
# Set execute path and default browser
    executable_path = {'executable_path': cdp}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:

def scrape():
    browser=init_browser()
    # mars_data={}
    # Set url for NASA Mars News Site
    mars_url='https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    # Set sleep time for 2 seconds
    time.sleep(2)
    html1=browser.html
    soup1=bs(html1,'html.parser')


    # In[4]:


    # Setting 'results' variable to find for the data
    results = soup1.find_all('li',attrs={'class':'slide'})


    # In[5]:


    # print(results)


    # In[6]:


    title=[]
    paragraphs=[]
    # Loop through the results
    for x in results:
        # Error handling
        try:
            news_title=x.find('div',attrs={'class':'content_title'}).get_text()
            news_p=x.find('div',attrs={'class':'article_teaser_body'}).get_text()
            title.append(news_title)
            paragraphs.append(news_p)
            if (news_title):
                print('-'*8)
                print(news_title)
                print(news_p)
        except AttributeError as e:
            print(e)

    # mars_data['Title']=title
    # mars_data['Paragraph']=paragraphs
    # In[7]:


    # JPL mars url
    mar_image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mar_image_url)
    browser.click_link_by_id('full_image')
    # Set sleep time for 2 seconds
    time.sleep(2)
    html2=browser.html
    soup2=bs(html2,'html.parser')
    # Setup the main url for the image.
    main_url='https://www.jpl.nasa.gov'

    image_url=soup2.find('img',attrs={'class':'fancybox-image'})['src']
    feature_image=main_url+image_url
    # mars_data['featured_image_url']=feature_image
    # print(feature_image)


    # In[8]:


    # Mars weather from Twitter
    weather_url='https://twitter.com/MarsWxReport?lang=en'
    browser.visit(weather_url)
    # Set delay time for 2 seconds
    time.sleep(2)
    html3=browser.html
    soup3=bs(html3,'html.parser')
    # Find the tweets
    weather_tweet=soup3.find('div',attrs={'class':'css-1dbjc4n'}).find('div',attrs={'class':'css-1dbjc4n'}).find('div',attrs={'class':'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'}).find('span',attrs={'class':'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})


    # In[9]:


    # print(weather_tweet)


    # In[10]:


    # Strip out the tweet from return output
    for mars_weather in weather_tweet:
        if mars_weather.strip().startswith('Sol'):
            weather_tweet=mars_weather.text.strip()

    # mars_data['weather_tweet']=mars_weather
    # In[11]:


    # print(mars_weather)


    # In[12]:


    # Read in the html site, then pick the first table
    mars_df=pd.read_html('https://space-facts.com/mars/')[0]
    # Setup the DataFrame
    mars_df.columns=['Description','Value']
    mars_df.set_index('Description',inplace=True)
    mars_fact = mars_df.to_html(classes='marsfact')
    mars_fact =mars_fact.replace('\n', ' ')


    # In[13]:


    # Mars hemispheres
    # hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_list=['Cerberus','Schiaparelli','Syrtis Major','Valles Marineris']
    search_url='https://astrogeology.usgs.gov/search/map/Mars/Viking/'
    image_title=[]
    image_url=[]
    hemisphere_dict=[]
    for hemisphere in hemi_list:
        browser.visit(search_url+hemisphere)
        time.sleep(2)
        html4=browser.html
        soup4=bs(html4,'lxml')
        img_title=soup4.find('h2',attrs={'class':'title'}).get_text()
        img_url=soup4.find('div',attrs={'class':'downloads'})                        .find('ul').find('li').find('a')['href']
        image_title.append(img_title)
        image_url.append(img_url)
        image_dictionary={'title':img_title,'img_url':img_url}
        hemisphere_dict.append(image_dictionary)
    mars_data={
        'Mars_title':title[0],
        'Mars_paragraph':paragraphs[0],
        'Mars_featured_image':feature_image,
        'Mars_fact':mars_fact,
        'Mars_tweet':mars_weather,
        'Mars_hemispheres':hemisphere_dict}
    browser.quit()
    return mars_data
# In[14]:


# # Create a list of dictionary for hemisphere
# hemisphere_dict=dict(zip(image_title,image_url))


# In[16]:


# Display the dictionary
    


# In[ ]:




