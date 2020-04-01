import config
import time

from mysql import connector

FILE = 'grad.csv'

db = connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    passwd=config.DB_PASS,
    database=config.DB_NAME
)

def main():
    cursor = db.cursor()
    with open(FILE, 'r') as f:
        positions = f.readlines()
        for position in positions:
            position = position.split(',')
            link = position[0]
            company = position[1]
            title = position[2]
            type = position[3]
            cursor.execute('INSERT INTO jobs (link, company, title, post_time, type) VALUES (%s, %s, %s, %s, %s)',
                (link, company, title, int(time.time()), type))
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
