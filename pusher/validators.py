def is_incomplete(job):
    required_fields = ['name', 'company_name', 'location', 'source_url', 'date_posted']
    for field in required_fields:
        if not job.get(field):
            print(f"⚠️ Missing field '{field}' in job: {job.get('name', 'UNKNOWN')}")
            return True
    return False
