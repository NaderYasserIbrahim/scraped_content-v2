from odoo import http
from odoo.http import request
import math

class ScrapedJobController(http.Controller):

    @http.route('/scraped-jobs', type='http', auth='public', website=True)
    def scraped_jobs(self, page=1, location=None, company=None, **kwargs):
        Job = request.env['scraped.job'].sudo()
        domain = [('status', '=', 'approved')]

        if location:
            domain.append(('location', 'ilike', location))
        if company:
            domain.append(('company_name', 'ilike', company))

        per_page = 5
        total = Job.search_count(domain)
        page_count = int(math.ceil(total / per_page))
        offset = (int(page) - 1) * per_page

        jobs = Job.search(domain, order='date_posted desc', limit=per_page, offset=offset)

        return request.render('scraped_content.jobs_page_template', {
            'jobs': jobs,
            'page': int(page),
            'page_count': page_count,
            'location_filter': location or '',
            'company_filter': company or '',
        })
