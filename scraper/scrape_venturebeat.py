import requests
from bs4 import BeautifulSoup
import csv

STATIC_PAGES = [
    'https://venturebeat.com/about/',
    'https://venturebeat.com/contact/',
    'https://venturebeat.com/privacy-policy/',
]

OUTPUT_FILE = '../data/venturebeat_pages.csv'

def scrape_static_pages():
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'content', 'source_url'])
        writer.writeheader()

        for url in STATIC_PAGES:
            print(f"Scraping: {url}")
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, 'html.parser')

                title = soup.title.string.strip() if soup.title else 'Untitled'
                content_div = soup.find('div', class_='article-content') or soup.find('main')
                if content_div:
                    paragraphs = content_div.find_all(['p', 'h2', 'li'])
                    content = "\n".join(p.get_text(strip=True) for p in paragraphs)
                else:
                    content = soup.get_text(strip=True)

                writer.writerow({
                    'title': title,
                    'content': content,
                    'source_url': url
                })

            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

    print(f"Static pages saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    scrape_static_pages()
