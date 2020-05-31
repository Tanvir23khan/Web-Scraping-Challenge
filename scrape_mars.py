#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

import pymongo
import requests
import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs


#################################################
# DB Setup
#################################################

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 


#################################################
# Windows-  Scrape Data
#################################################

# executable_path = {'executable_path': 'chromedriver.exe'}
def scrape():

	collection.drop()
    
	executable_path = {'executable_path':'C:/Users/h_23m/Desktop/Web-Scraping-Challenge/chromedriver.exe'}
	

	browser = Browser('chrome', **executable_path, headless=False)

#################################################
# NASA Mars News
#################################################

	news_url ="https://mars.nasa.gov/news/"
	browser.visit(news_url)
	time.sleep(3)
	news_html = browser.html
	nsoup = bs(news_html,'lxml')
	news_results = nsoup.find_all('div', class_='list_text')
	latest_news = news_results[0]
	news_title = latest_news.find("div", class_="content_title").text
	news_p = nsoup.find('div', class_='article_teaser_body').text
	print(f"Title:\n\n{news_title}")
	print("\n-------------------------------------------------------------------------------------------\n")
	print(f"Paragraph:\n\n{news_p}")


#################################################
# JPL Mars Space Images - Featured Image
#################################################

	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl_url)
	time.sleep(2)
	jpl_html = browser.html
	jsoup = bs(jpl_html,'lxml')
	img_link = jsoup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
	base_link = jsoup.find('div', class_='jpl_logo').a['href'].rstrip('/')
	featured_image_title = jsoup.find('h1', class_="media_feature_title").text.strip()
	featured_image_url = base_link + img_link
	print(f"Featured Image URL:\n\n{featured_image_url}")
	print("\n---------------------------------------------------------------------------------------------\n")
	print(f"Featured Image Title:\n\n{featured_image_title}")


#################################################
# Mars Weather
#################################################

	weather_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(weather_url)
	time.sleep(3)
	w_html = browser.html
	wsoup = bs(w_html,'lxml')
	tweets = wsoup.find_all('span', class_= "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
	for tweet in tweets:
		tweet_text = tweet.text
		if 'sol' in tweet_text and 'pressure' in tweet_text:
			mars_weather = tweet_text
			print(f"Mars Weather Twitter Tweet:\n\n{tweet_text}")
			break
		else:
			pass

#################################################
# Mars Facts
#################################################

	fact_url = "http://space-facts.com/mars/"
	fact_table = pd.read_html(fact_url)
	time.sleep(2)
	print(fact_table)
	mars_fact_table = fact_table[0]
	print(mars_fact_table)
	mars_fact_table.columns=["Description", "Value"]
	mars_fact_table.set_index("Description", inplace=True)
	print(mars_fact_table)
	mars_fact_table_html = mars_fact_table.to_html(header=False, index=True)
	mars_fact_table_html = mars_fact_table_html.replace('\n', '')
	print(f"Mars facts HTML table:")
	print("\n------------------------------------------------------------------------------------------------\n")
	print(f"{mars_fact_table_html}")


#################################################
# Mars Hemispheres
#################################################
	hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hem_url)
	time.sleep(2)
	urls = [(a.text, a['href']) for a in browser
	         .find_by_css('div[class="description"] a')]
	hemisphere_image_urls = []
	for title,url in urls:
	    product_dict = {}
	    product_dict['title'] = title
	    browser.visit(url)
	    img_url = browser.find_by_css('img[class="wide-image"]')['src']
	    product_dict['img_url'] = img_url
	    hemisphere_image_urls.append(product_dict)
	print(f"Hemisphere Image URLs")
	print("\n------------------------------------------------------------------------------------------------\n")

	print(f"Cerberus Hemisphere Enhanced:\n{hemisphere_image_urls[0]}\n")

	print(f"Schiaparelli Hemisphere Enhanced:\n{hemisphere_image_urls[1]}\n")

	print(f"Syrtis Major Hemisphere Enhanced:\n{hemisphere_image_urls[2]}\n")

	print(f"Valles Marineris Hemisphere Enhanced:\n{hemisphere_image_urls[3]}\n")

	browser.quit()

#################################################
# pack the return dictionary
#################################################

	mars_data ={
		'news_title' : news_title,
		'summary': news_p,
		'featured_image': featured_image_url,
		'featured_image_title': featured_image_title,
		'weather': mars_weather,
		'fact_table': mars_fact_table_html,
		'hemisphere_image_urls': hemisphere_image_urls,
        'news_url': news_url,
        'jpl_url': jpl_url,
        'weather_url': weather_url,
        'fact_url': fact_url,
        'hemisphere_url': hem_url,
	}


	# return mars_data

	collection.insert(mars_data)
    
# if __name__ == "__main__":
	# scrape()