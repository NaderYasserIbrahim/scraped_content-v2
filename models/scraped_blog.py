import csv
import logging
from datetime import datetime
from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)

class ScrapedBlog(models.Model):
    _name = 'scraped.blog'
    _description = 'Blog Posts Scraped'

    title = fields.Char(string='Title', required=True)
    summary = fields.Text(string='Summary')
    content = fields.Text(string='Content')
    source_url = fields.Char(string='Source URL')
    date_published = fields.Datetime(string='Published Date')
    pushed = fields.Boolean(string='Pushed to Website', default=False)

    status = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('archived', 'Archived')
    ], default='new', string='Status')

    @api.model
    def manually_import_blogs_from_csv(self):
        csv_path = tools.misc.file_open('scraped_content/data/techcrunch_blogs.csv').name

        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    date_published = False
                    raw_date = row.get('date_published', '')
                    if raw_date:
                        try:
                            date_published = datetime.strptime(raw_date.strip(), '%a, %d %b %Y %H:%M:%S %z')
                        except ValueError as e:
                            _logger.warning(f"Invalid date '{raw_date}': {e}")
                            continue

                    vals = {
                        'title': row.get('title', '').strip(),
                        'summary': row.get('summary', '').strip(),
                        'content': row.get('content', '').strip(),
                        'source_url': row.get('source_url', '').strip(),
                        'date_published': date_published,
                        'status': 'new',
                        'pushed': False,
                    }

                    if self.search_count([
                        ('title', '=', vals['title']),
                        ('source_url', '=', vals['source_url']),
                    ]):
                        _logger.info(f"Skipped duplicate: {vals['title']}")
                        continue

                    self.create(vals)
                _logger.info("CSV blog import complete.")
        except Exception as e:
            _logger.error(f"Failed to import blog CSV: {e}")

        return True
