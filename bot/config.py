import os

# base url
LI_BASE_URL = 'https://www.linkedin.com/comm/jobs/view/'

# email
EMAIL = os.environ.get('email')
PASS = os.environ.get('email_pass')
FROM = 'jobalerts-noreply@linkedin.com'

# database
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'root'
DB_NAME = 'LinkedinJobAlerts'
