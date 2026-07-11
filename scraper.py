import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.robotparser

BASE_URL = "https://books.toscrape.com/"

# Check robots.txt
rp = urllib.robotparser.RobotFileParser()
rp.set_url(BASE_URL + "robots.txt")
rp.read()

if not rp.can_fetch("*", BASE_URL):
    print("Scraping not allowed by robots.txt")
    exit()

print("robots.txt check passed")

headers = {
    "User-Agent": "FlyRank-Intern-Scraper/1.0 (Educational Project)"
}

response = requests.get(BASE_URL, headers=headers)

if response.status_code != 200:
    print("Failed to fetch page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

books = []

for book in soup.select(".product_pod"):
    title = book.h3.a["title"].strip()
    price = book.select_one(".price_color").text.strip()
    availability = book.select_one(".availability").text.strip()

    books.append({
        "Title": title,
        "Price": price,
        "Availability": availability
    })

    # Rate limiting
    time.sleep(1)

df = pd.DataFrame(books)
df.to_csv("data.csv", index=False)

print(f"Saved {len(books)} books to data.csv")