import imaplib
import email
import sys
import re
import config
import requests
import time

from datetime import datetime, date, timedelta
from db import save_new_jobs
from bs4 import BeautifulSoup


def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])


def get_yesterday(fmt="%d-%b-%Y"):
    return (datetime.now() - timedelta(1)).strftime(fmt)


def get_connection(email_addr, password):
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(email_addr, password)
    conn.select()
    return conn


def load_emails(conn, from_client):
    command = '(SINCE "{0}")'.format(get_yesterday())
    typ, data = conn.search(None, command)
    emails = []

    try:
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    subject = msg['subject']
                    payload = msg.get_payload()
                    body = extract_body(payload)
                    emails.append((subject, body))
    finally:
        try:
            conn.close()
        except:
            pass

    return emails

def find_job_ids(emails, base=config.LI_BASE_URL):
    all_job_ids = set()

    for em in emails:
        urls = re.findall(base+r"\d+", em[1])
        job_ids = set([x.split('/')[-1] for x in urls if len(x.split('/')[-1]) == 10])
        all_job_ids |= job_ids

    return all_job_ids

# rude approximation of post date, extracted from linkedin 'ago' string
def extract_time(soup):
    ago_string = '1 minute ago'

    try:
        ago_string = soup.find(class_='topcard__flavor--metadata posted-time-ago__text').string
    except Exception:
        ago_string = soup.find(class_='topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new').string

    print(ago_string)
    parts = ago_string.strip().split(' ')
    time_stamp = int(time.time())
    offset = 1

    if parts[1] == 'minutes' or parts[1] == 'minute':
        offset = 60
    elif parts[1] == 'hours' or parts[1] == 'hour':
        offset = 3600
    elif parts[1] == 'days' or parts[1] == 'day':
        offset = 86400
    elif parts[1] == 'weeks' or parts[1] == 'week':
        offset = 604800
    elif parts[1] == 'months' or parts[1] == 'month':
        offset = 2419200
    elif parts[1] == 'years':
        offset = 29030400

    offset *= int(parts[0])
    print(offset)
    return time_stamp - offset


def extract_type(title):
    title = title.lower()
    if 'intern' in title:
        return 1
    elif 'graduate' in title and 'software' in title:
        return 2
    else:
        return 3


def jobs_from_ids(job_ids):
    jobs = []
    for job_id in job_ids:
        try:
            jobs.append(job_from_id(job_id))
        except Exception:
            pass
    return jobs


def extract_company(soup):
    companies = soup.select('a[class*="topcard__org-name-link"]')
    return companies[0].string if companies else "Unknown"


def job_from_id(job_id, base=config.LI_BASE_URL):
    print(f'{base}{job_id}')
    r = requests.get(f'{base}{job_id}')
    soup = BeautifulSoup(r.text, 'html.parser')
    company = extract_company(soup)
    title = soup.find(class_='topcard__title').string
    print(job_id)
    print(company)
    print(title)
    post_time = extract_time(soup)
    job_type = extract_type(title)
    return (base + str(job_id)), company, title, post_time, job_type


def main(args):
    con = get_connection(config.EMAIL, config.PASS)
    emails = load_emails(con, config.FROM)
    print("LEN EMAILS: {0}".format(len(emails)))
    job_ids = find_job_ids(emails)
    jobs = jobs_from_ids(job_ids)
    save_new_jobs(jobs)


if __name__ == '__main__':
    main(sys.argv)
