import requests
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
import psycopg2
from psycopg2 import sql
import os
from sqlalchemy import create_engine
import time

keywords = ['election', 'war', 'economy']
urls = {
    'https://www.ft.com': 'ft',
    'https://www.theguardian.com/europe': 'guardian'
}

dbname=os.getenv('DB_NAME', 'keywords'),
user=os.getenv('DB_USER', 'admin'),
password=os.getenv('DB_PASS', 'admin'),
host=os.getenv('DB_HOST', 'db'),  
port=os.getenv('DB_PORT', '5432')

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname)
db = create_engine(db_string)

def connect_db():
    return psycopg2.connect(
        #dbname='keywords',
        #user='admin',  
        #password='admin',
        #host='localhost',
        #port='5432' 
        dbname=os.getenv('DB_NAME', 'keywords'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASS', 'admin'),
        host=os.getenv('DB_HOST', 'db'),  
        port=os.getenv('DB_PORT', '5432')
    )


def count_keywords_in_headings(url, keywords, site_name):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None
    
    if url == 'https://www.ft.com':
        soup = BeautifulSoup(response.content, 'lxml')
        headings = []

        for span in soup.select('span.text.text--color-black.text--weight-500, span.text.text--color-black.text--weight-400'):
            # Check if the next span is a subheading
            next_span = span.find_next('span', class_='text-sans--scale-5')
            if not next_span:
                headings.append(span.get_text(strip=True))
                #print("Found heading:", span.get_text(strip=True))
        
        headings_text = ' '.join([heading.lower() for heading in headings])
        keyword_count = Counter({keyword: headings_text.count(keyword) for keyword in keywords})
        timestamp = datetime.now()
    
        results = [
            {"term": keyword, "incidence": count, "site": site_name, "timestamp": timestamp}
            for keyword, count in keyword_count.items()
        ]

    elif url == 'https://www.theguardian.com/europe':
        
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = soup.find_all('h3')
        
        headings_text = ' '.join([heading.get_text().lower() for heading in headings])
        keyword_count = Counter({keyword: headings_text.count(keyword) for keyword in keywords})
        timestamp = datetime.now()
    
        results = [
            {"term": keyword, "incidence": count, "site": site_name, "timestamp": timestamp}
            for keyword, count in keyword_count.items()
        ]
    
    return results

def insert_data(data):
    conn = connect_db()
    cur = conn.cursor()
    
    insert_query = sql.SQL("""
        INSERT INTO search_data (term, incidence, site, timestamp)
        VALUES (%s, %s, %s, %s)
    """)
    
    for entry in data:
        cur.execute(insert_query, (entry['term'], entry['incidence'], entry['site'], entry['timestamp']))
    
    conn.commit()
    cur.close()
    conn.close()

def main():
    all_results = []

    for url, site_name in urls.items():
        results = count_keywords_in_headings(url, keywords, site_name)
        if results:
            all_results.extend(results)
    
    if all_results:
        insert_data(all_results)
        print("Data inserted successfully.")
    else:
        print("No data to insert.")

if __name__ == '__main__':
    main()
    while True:
        time.sleep(100)
