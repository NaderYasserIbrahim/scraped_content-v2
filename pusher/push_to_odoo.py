import os
import csv
import xmlrpc.client
from dotenv import load_dotenv
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from validators import is_incomplete

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_exception_type(Exception))
def safe_execute_kw(model_proxy, *args, **kwargs):
    return model_proxy.execute_kw(*args, **kwargs)

# Load environment variables
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
DB = os.getenv("ODOO_DB")
USERNAME = os.getenv("ODOO_USER")
PASSWORD = os.getenv("ODOO_PASSWORD")

# Model → CSV path mapping
MODELS = {
    'jobs': ('scraped.job', 'data/linkedin_jobs.csv'),
    'blogs': ('scraped.blog', 'data/techcrunch_blogs.csv'),
    'pages': ('scraped.page', 'data/venturebeat_pages.csv'),
}

def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', relative_path))

def authenticate():
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    if not uid:
        raise Exception("❌ Authentication failed.")
    print(f"✅ Authenticated with UID: {uid}")
    return uid

def push_data(uid, model_name, csv_path):
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    abs_csv_path = get_absolute_path(csv_path)

    with open(abs_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            vals = {}

            if model_name == 'scraped.job':
                vals = {
                    'name': row.get('Job Title', '').strip(),
                    'company_name': row.get('Company Name', '').strip(),
                    'company_logo_url': row.get('Company Logo', '').strip(),
                    'location': row.get('Location', '').strip(),
                    'source_url': row.get('Source URL', '').strip(),
                    'status': 'new',
                }
                posted = row.get('Posted Date', '').strip()
                if posted:
                    try:
                        vals['date_posted'] = datetime.strptime(posted, "%Y-%m-%d")
                    except Exception:
                        pass

            elif model_name == 'scraped.blog':
                vals = {
                    'title': row.get('title', '').strip(),
                    'summary': row.get('summary', '').strip(),
                    'content': row.get('content', '').strip(),
                    'source_url': row.get('source_url', '').strip(),
                    'status': 'new',
                }

            elif model_name == 'scraped.page':
                vals = {
                    'title': row.get('title', '').strip(),
                    'content': row.get('content', '').strip(),
                    'source_url': row.get('source_url', '').strip(),
                    'status': 'new',
                }

            # Skip incomplete entries
            if not vals.get('title') or not vals.get('source_url'):
                print(f"⚠️ Skipping incomplete: {vals}")
                continue

            # Skip duplicates
            existing = safe_execute_kw(models,DB, uid, PASSWORD, model_name, 'search_count', [[
                ('title' if 'title' in vals else 'name', '=', vals.get('title') or vals.get('name')),
                ('source_url', '=', vals['source_url'])
            ]])
            if existing:
                print(f"⏭ Skipped duplicate: {vals.get('title') or vals.get('name')}")
                continue

            safe_execute_kw(models,DB, uid, PASSWORD, model_name, 'create', [vals])
            count += 1

        print(f"✅ {count} records pushed to {model_name}")

def push_blog_to_website(uid, password):
    print("🔄 Syncing scraped.blog to website.blog.post...")

    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

    blog_posts = safe_execute_kw(models,DB, uid, password, 'scraped.blog', 'search_read',
        [[('status', '=', 'approved'), ('pushed', '=', False)]],
        {'fields': ['id', 'title', 'summary', 'content', 'source_url', 'date_published']}
    )

    for blog in blog_posts:
        existing = safe_execute_kw(models,DB, uid, password, 'blog.post', 'search_count', [[
            ('name', '=', blog['title']),
            ('website_url', 'ilike', blog['source_url'])
        ]])
        if existing:
            print(f"⏭ Skipped existing blog: {blog['title']}")
            continue

        values = {
            'name': blog['title'],
            'subtitle': blog.get('summary', ''),
            'content': blog.get('content', ''),
            'website_published': True,
            'website_url': blog['source_url'],
            'post_date': blog.get('date_published') or None,
        }

        safe_execute_kw(models,DB, uid, password, 'blog.post', 'create', [values])
        print(f"✅ Blog published: {blog['title']}")

        # 🔄 Mark as pushed
        safe_execute_kw(models,DB, uid, password, 'scraped.blog', 'write', [[blog['id']], {'pushed': True}])


def push_pages_to_website(uid, password):
    print("🔄 Syncing scraped.page to website.page...")

    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

    pages = safe_execute_kw(models,DB, uid, password, 'scraped.page', 'search_read',
        [[('status', '=', 'approved'), ('pushed', '=', False)]],
        {'fields': ['id', 'title', 'content', 'source_url']}
    )

    for page in pages:
        exists = safe_execute_kw(models,DB, uid, password, 'website.page', 'search_count', [[
            ('name', '=', page['title'])
        ]])
        if exists:
            print(f"⏭ Skipped existing page: {page['title']}")
            continue

        values = {
            'name': page['title'],
            'url': '/' + page['title'].strip().lower().replace(' ', '-'),
            'website_published': True,
            'content': page['content'] or '',
        }

        safe_execute_kw(models,DB, uid, password, 'website.page', 'create', [values])
        print(f"✅ Page published: {page['title']}")

        # 🔄 Mark as pushed
        safe_execute_kw(models,DB, uid, password, 'scraped.page', 'write', [[page['id']], {'pushed': True}])

# MAIN RUNNER
if __name__ == '__main__':
    try:
        uid = authenticate()
        for label, (model_name, csv_file) in MODELS.items():
            print(f"\n📦 Pushing {label} from {csv_file} into {model_name}...")
            push_data(uid, model_name, csv_file)

        push_blog_to_website(uid, PASSWORD)
        push_pages_to_website(uid, PASSWORD)

    except Exception as e:
        print(f"❌ Error: {e}")
