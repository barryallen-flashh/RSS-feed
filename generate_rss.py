import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

def fetch_articles():
    url = "https://cybersecurityventures.com/cybercrime-news/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []

    for item in soup.select("div.post-content"):
        title_tag = item.find("a")
        date_tag = item.find("time")
        if title_tag and title_tag.get("href"):
            title = title_tag.text.strip()
            link = title_tag["href"].strip()
            pubdate = date_tag.get("datetime") if date_tag else datetime.utcnow().isoformat()

            articles.append({
                "title": title,
                "link": link,
                "published": pubdate
            })

    return articles

def generate_rss(articles):
    fg = FeedGenerator()
    fg.title("Cybercrime News - Cybersecurity Ventures")
    fg.link(href="https://cybersecurityventures.com/cybercrime-news/")
    fg.description("Latest cybercrime news from Cybersecurity Ventures.")
    fg.language("en")
    fg.ttl(60)  # Refresh every 60 minutes

    for article in articles:
        fe = fg.add_entry()
        fe.title(article["title"])
        fe.link(href=article["link"])
        fe.published(article["published"])

    fg.rss_file("cybercrime_news.xml")
    print("RSS feed generated.")

if __name__ == "__main__":
    articles = fetch_articles()
    generate_rss(articles)
