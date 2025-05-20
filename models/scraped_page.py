import csv
import logging
from odoo import models, fields, api, tools
import os

_logger = logging.getLogger(__name__)

class ScrapedPage(models.Model):
    _name = 'scraped.page'
    _description = 'Static Web Page Scraped'

    title = fields.Char(string='Page Title', required=True)
    content = fields.Text(string='Content')
    source_url = fields.Char(string='Source URL')
    pushed = fields.Boolean(string='Pushed to Website', default=False)
    status = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('archived', 'Archived')
    ], default='new', string='Status')

    @api.model
    def manually_import_pages_from_csv(self):
        base_path = os.path.dirname(__file__)
        csv_path = os.path.abspath(os.path.join(base_path, '..', 'data', 'venturebeat_pages.csv'))

        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if self.search_count([
                        ('title', '=', row['title']),
                        ('source_url', '=', row['source_url'])
                    ]):
                        continue

                    self.create({
                        'title': row['title'].strip(),
                        'content': row.get('content', '').strip(),
                        'source_url': row['source_url'].strip(),
                        'status': 'new',
                        'pushed': False,
                    })

            _logger.info(" Page import from CSV complete.")
        except Exception as e:
            _logger.error(f" Failed to import pages: {e}")
