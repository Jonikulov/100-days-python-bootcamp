"""Day 45. Web Scraping with Beautiful Soup"""

import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

# Getting Hacker News, descending order by upvotes
articles = soup.select("td.title span.titleline > a")
upvotes = soup.select("td.subtext span.score")
news_data = []
for article, upvote in zip(articles, upvotes):
    news_data.append({
        "title": article.get_text(strip=True),
        "upvote": int(upvote.get_text(strip=True).split()[0]),
        "url": article.get("href"),
    })
news_data.sort(key=lambda x: x["upvote"], reverse=True)

for idx, news in enumerate(news_data, start=1):
    print(f"\n{idx}. TITLE:", news["title"])
    print("UPVOTE:", news["upvote"])
    print("URL:", news["url"])
