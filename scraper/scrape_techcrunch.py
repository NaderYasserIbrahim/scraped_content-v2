import feedparser
import requests
from bs4 import BeautifulSoup
import csv

RSS_FEED = 'https://techcrunch.com/feed/'
OUTPUT_FILE = '../data/techcrunch_blogs.csv'

def scrape_techcrunch_rss():
    feed = feedparser.parse(RSS_FEED)

    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'title', 'summary', 'content', 'date_published', 'source_url'
        ])
        writer.writeheader()

        for entry in feed.entries:
            title = entry.title
            summary = entry.summary
            date_published = entry.published
            source_url = entry.link

            # Fetch full article content
            content = ''
            try:
                response = requests.get(source_url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.select('div.article-content p')
                content = "\n".join(p.get_text(strip=True) for p in paragraphs)
            except Exception as e:
                print(f"Error fetching full content: {e}")

            writer.writerow({
                'title': title,
                'summary': summary,
                'content': content,
                'date_published': date_published,
                'source_url': source_url
            })

    print(f"Saved blog posts to {OUTPUT_FILE}")

if __name__ == '__main__':
    scrape_techcrunch_rss()
