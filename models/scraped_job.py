import csv
import logging
from datetime import datetime
from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)

class ScrapedJob(models.Model):
    _name = 'scraped.job'
    _description = 'Job Postings Scraped'

    name = fields.Char(string='Job Title', required=True)
    company_name = fields.Char(string='Company Name')
    company_logo_url = fields.Char(string='Company Logo URL')
    location = fields.Char(string='Location')
    source_url = fields.Char(string='Source URL')
    date_posted = fields.Datetime(string='Posted Date')
    status = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('archived', 'Archived')
    ], default='new', string='Status')

    @api.model
    def manually_import_jobs_from_csv(self):
        # Get the actual file path using get_module_resource for cross-platform support
        csv_path = tools.misc.file_open('scraped_content/data/linkedin_jobs.csv').name

        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Parse date
                    date_posted = False
                    raw_date = row.get('Posted Date', '')
                    if raw_date:
                        try:
                            date_posted = datetime.strptime(raw_date.strip(), '%Y-%m-%d')
                        except ValueError as e:
                            _logger.warning(f"Invalid date '{raw_date}': {e}")
                            continue

                    # Construct record values
                    vals = {
                        'name': row.get('Job Title', '').strip(),
                        'company_name': row.get('Company Name', '').strip(),
                        'company_logo_url': row.get('Company Logo', '').strip(),
                        'location': row.get('Location', '').strip(),
                        'source_url': row.get('Source URL', '').strip(),
                        'date_posted': date_posted,
                        'status': 'new',
                    }

                    # Optional: Skip if already exists (based on title + company + date)
                    if self.search_count([
                        ('name', '=', vals['name']),
                        ('company_name', '=', vals['company_name']),
                        ('date_posted', '=', vals['date_posted'])
                    ]):
                        _logger.info(f"Skipped duplicate: {vals['name']}")
                        continue

                    self.create(vals)
                _logger.info("CSV import complete.")
        except Exception as e:
            _logger.error(f"Failed to import CSV: {e}")

        return True
