import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape product titles and prices from a demo e-commerce site
URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

products = []
for item in soup.select(".thumbnail"):
    title = item.select_one(".title").get("title")
    price = item.select_one(".price").text.strip()
    products.append({"title": title, "price": price})

df = pd.DataFrame(products)
df.to_csv("laptop_prices.csv", index=False)
print(f"Scraped {len(df)} products. Data saved to laptop_prices.csv") 