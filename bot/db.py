import config
import time

from mysql import connector

DB = connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    passwd=config.DB_PASS,
    database=config.DB_NAME
)


def get_cursor():
    return DB.cursor(dictionary=True)


def close(db):
    db.close()


def save_new_jobs(jobs, db=DB):
    cursor = get_cursor()

    for job in jobs:
        link = job[0]
        cursor.execute('SELECT link FROM jobs WHERE link = %s', (link,))
        if cursor.fetchone() is None:  # job is new
            cursor.execute('INSERT INTO jobs (link, company, title, post_time, type) VALUES (%s, %s, %s, %s, %s)',
            (link, job[1], job[2], job[3], job[4]))
            db.commit()

    close(db)


def get_internships():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM jobs WHERE post_time BETWEEN %s AND %s AND type = 1', (int(time.time()) - 3 * 2419200, int(time.time())))
    return cursor.fetchall()


def get_grads():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM jobs WHERE post_time BETWEEN %s AND %s AND type = 2', (int(time.time()) - 3 * 2419200, int(time.time())))
    return cursor.fetchall()


def get_swes():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM jobs WHERE post_time BETWEEN %s AND %s AND type = 1', (int(time.time()) - 3 * 2419200, int(time.time())))
    return cursor.fetchall()


def get_all():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM jobs WHERE post_time BETWEEN %s AND %s', (int(time.time()) - 3 * 2419200, int(time.time())))
    return cursor.fetchall()
