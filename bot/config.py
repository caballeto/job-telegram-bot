import os

# base url
LI_BASE_URL = 'https://www.linkedin.com/comm/jobs/view/'

# email
EMAIL = os.environ.get('EMAIL')
PASS = os.environ.get('EMAIL_PASS')
FROM = 'jobalerts-noreply@linkedin.com'

# database
DB_HOST = 'localhost'
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = 'LinkedinJobAlerts'
