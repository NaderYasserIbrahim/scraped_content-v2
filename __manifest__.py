{
    'name': 'Scraped Content',
    'version': '1.1',
    'category': 'Custom',
    'summary': 'Manage and publish scraped jobs, blogs, and pages',
    'description': '''
        A modular solution to manage web-scraped job listings, blog posts, and static pages.
        Content can be imported, reviewed, and published to the Odoo website.
    ''',
    'author': 'Your Name',
    'depends': [
        'base',
        'website',
        'website_blog',  # Required for publishing blog posts
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/scraped_content_views.xml',
        'views/scraped_blog_views.xml',
        'views/scraped_page_views.xml',
        'templates/jobs_page.xml',
        'views/website_menu.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
