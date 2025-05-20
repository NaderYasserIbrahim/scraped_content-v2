# 🧩 Odoo Web Scraping & Integration Project

This project is a modular solution for scraping external web content (jobs, blogs, and pages), pushing that content into a custom Odoo module, and optionally publishing it to the Odoo Website.

---

## 🛠️ Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/odoo-scraper-project.git
   cd odoo-scraper-project
### 2. Create a virtual environment & install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```
### 3. Add environment variables:

- Create a `.env` file with the following content:

```ini
ODOO_URL=http://localhost:8069
ODOO_DB=your_database_name
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password
```

## 🏃 How to Run Scrapers

Navigate to the `/scrapers` folder and run each scraper manually:

```bash
cd scrapers
python linkedin_jobs.py
python techcrunch_blogs.py
python venturebeat_pages.py
```

## 🚀 How to Run the Pusher Script

```bash
cd pusher
python push_to_odoo.py
```

## 📦 How to Install the Odoo Module

1. Copy the `scraped_content` folder into your Odoo `addons` directory.
2. Restart Odoo and update the apps list.
3. Install the **Scraped Content** module from the Apps menu.


## 🌐 How to See the Data on Odoo Website

- Blog data appears in `website.blog.post`
- Page content appears in `website.page`
- Job data can be rendered as static pages or in a custom listing view


## 📁 Project Structure

```bash
/scrapers/
  linkedin_jobs.py
  techcrunch_blogs.py
  venturebeat_pages.py

/pusher/
  push_to_odoo.py
  .env

/scraped_content/
  __manifest__.py
  /models/
    scraped_job.py
    scraped_blog.py
    scraped_page.py
  /views/
    scraped_job_views.xml
    scraped_blog_views.xml
    scraped_page_views.xml
  /security/
    ir.model.access.csv

README.md
```
## ✅ Used Tools & Libraries

| Purpose              | Tool/Library               | Notes                                         |
|----------------------|----------------------------|-----------------------------------------------|
| HTTP Requests        | `requests`                 | For static pages                              |
| HTML Parsing         | `BeautifulSoup`            | Clean and simple HTML parser                  |
| Structured Crawling  | `Scrapy`                   | For complex sites                             |
| JS Rendering         | `Playwright` / `Selenium`  | For dynamic pages like LinkedIn               |
| Data Storage         | `SQLite3` / `JSON`         | Lightweight and structured format             |
| Logging              | `logging`                  | Debugging and retry support                   |
| Odoo API Access      | `xmlrpc.client` / `requests` | XML-RPC or manual JSON-RPC payloads         |
| Env Configuration    | `dotenv`                   | Secure credentials                            |
| Retry Logic          | `tenacity`                 | Optional retry for unstable endpoints         |


