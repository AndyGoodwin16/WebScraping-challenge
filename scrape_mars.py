import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time
from bs4 import BeautifulSoup as bs

def scrape():
    #Set up Splinter.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visited url.
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)
    time.sleep(1)

    #Scraped page into Soup.
    html1 = browser.html
    soup1 = bs(html1, "html.parser")
    
    #Saved data into news_titles and news_p.
    results1a = soup1.find('div', class_='content_title')
    news_title = results1a.text
    
    results1b = soup1.find('div', class_='article_teaser_body')
    news_p = results1b.text
    
    #Visited url.
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)
    time.sleep(1)
    
    #Scraped page into Soup.
    html2 = browser.html
    soup2 = bs(html2, "html.parser")
    
    #Saved data in featured_image_url.
    results2 = soup2.find('img', class_='headerimage fade-in')
    featured_image_url = f"{url2}{results2['src']}"
    
    #Visited url.
    url3 = "https://galaxyfacts-mars.com/"
    browser.visit(url3)
    time.sleep(1)
    
    #Scraped page into Soup.
    html3 = browser.html
    soup3 = bs(html3, "html.parser")
    
    #Saved table to mars_table_html.
    table = pd.read_html(url3)
    mars_table = table[1]
    mars_table = mars_table.rename(columns={0:"Description", 1:"Measurement"})
    mars_table_html = mars_table.to_html(index=False)
    
    #Visited url.
    url4 = "https://marshemispheres.com/"
    browser.visit(url4)
    time.sleep(1)
    
    #Scraped page into Soup.
    html4 = browser.html
    soup4 = bs(html4, "html.parser")
    
    #Saved hemispheres names to hemispheres_list2.
    hemispheres = soup4.find_all('h3')
    hemispheres = hemispheres[0:4]
    
    hemispheres_list = []
    for i in range(len(hemispheres)):
        hemispheres_list.append(hemispheres[i].text)
        
    hemispheres_list2 = []
    for i in range(len(hemispheres_list)):
        n = hemispheres_list[i].replace(" Enhanced", "")
        hemispheres_list2 += [n]

    #Clicked on each hemisphere, then scraped image url.    
    image_urls_list = []
    for i in range(len(hemispheres_list2)):
        browser.find_by_css('h3')[i].click()
        n = browser.find_by_css('img.wide-image')['src']
        image_urls_list.append(n)
        browser.back()

    #Created list of dictionaries of hemispheres titles and urls to their image.    
    hemispheres_image_urls = []
    for i in range(len(hemispheres_list2)):
        n = {f'title': hemispheres_list2[i], 'img_url': image_urls_list[i]}
        hemispheres_image_urls.append(n)
    
    #Organized all data into a dictionary.
    mars_data = {"NewsTitle": news_title,
            "NewsParagraph": news_p,
            "FeaturedImageURL": featured_image_url,
            "InfoTable": mars_table_html,
            "HemispheresImageURLs": hemispheres_image_urls}
    
    browser.quit()
    
    return mars_data
            