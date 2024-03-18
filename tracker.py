import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time

base_url = "https://auctions.yahoo.co.jp/category/list/2084216953/?p=ビカクシダ、コウモリラン&auccat=2084216953&is_postage_mode=1&dest_pref_code=13&exflg=1&b={}&n=50&s1=featured"
# URL with a place holder{}, we can manipulate the page number 
items_per_page = 50
total_pages = 18  # Adjust based on how many pages you want to scrape
data = []
for page in range(1, total_pages + 1):
    start_index = (page - 1) * items_per_page + 1
    url = base_url.format(start_index)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    
    product_detail = soup.find_all('div', class_='Product__detail')
    for content in product_detail:
        
        # product name
        product = content.find('a')
        product_txt = product.text.strip()
        
        # current price
        now_price = content.find('span',class_="Product__priceValue u-textRed")
        now_price_txt = now_price.text.strip()
        
        # to check if there is a future price of the product
        future_price_tags = content.find_all('span', class_='Product__priceValue') # including current price tags
        future_price = "Price is determined"  # Default if no future price or indication is found
        for tag in future_price_tags:
            if 'u-textRed' not in tag['class']:  # Avoid re-selecting the current price
                future_price = f'New price:{tag.text.strip()}'
                break
                
                
        # bidding duration
        bidding_time = content.find('dd',class_="Product__time")
        bidding_time_txt = bidding_time.text.strip()
        
        # number of bidder
        bidder = content.find('dd',class_="Product__bid")
        bidder_txt = bidder.text.strip()
    
        # get herf
    
        herf = content.find('a')['href']
        
        # image URL then use API like Flask to read the collective URLs
        image_tag = content.find('a', class_='Product__titleLink')
        image_url = image_tag['data-auction-img'] if image_tag else None
        
    
        data.append({"Product":product_txt,"Now_price":now_price_txt,"Status":future_price,"bidding_duration":bidding_time_txt,"Number of bidder":bidder_txt,"herf":herf,"image":image_url})

    print(f"Scraping page {page} with URL: {url}")
    # Make sure to include a delay between requests to respect the website's server
    time.sleep(1)
