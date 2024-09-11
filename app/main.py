from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
from collections import Counter
from psycopg2 import sql
import os
from sqlalchemy import create_engine, text
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define time zone
tz = pytz.timezone('Europe/Tallinn') 

load_dotenv()
# Environment variables
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

# URLs and keywords
keywords = ['election', 'war', 'economy']
urls = {
    'https://www.ft.com': 'ft',
    'https://www.theguardian.com/europe': 'guardian'
}

# Database connection
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname)
db_engine = create_engine(db_string)

def count_keywords_in_headings(url, keywords, site_name):
    try:
        session = requests.Session()  # session to handle cookies
        response = session.get(url)
        response.raise_for_status()  

        if url == 'https://www.ft.com':
            soup = BeautifulSoup(response.content, 'lxml')
            headings = [span.get_text(strip=True) for span in soup.select('span.text.text--color-black.text--weight-500, span.text.text--color-black.text--weight-400') if not span.find_next('span', class_='text-sans--scale-5')]
            if not headings:
                logging.warning(f"No headings found at {url}")
                return []
        elif url == 'https://www.theguardian.com/europe':
            soup = BeautifulSoup(response.text, 'html.parser')
            headings = [heading.get_text().lower() for heading in soup.find_all('h3')]
        
        headings_text = ' '.join(headings).lower()
        keyword_count = Counter({keyword: headings_text.count(keyword) for keyword in keywords})

        timestamp = datetime.now(tz)
        
        results = [
            {"term": keyword, "incidence": count, "site": site_name, "timestamp": timestamp}
            for keyword, count in keyword_count.items()
        ]

        logging.info(f"Results for site: {site_name}")
        for result in results:
            logging.info(f"Keyword: {result['term']}, Count: {result['incidence']}, Timestamp: {result['timestamp']}")
        
        return results

    except requests.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return None

def insert_data(data):
    try:
        with db_engine.begin() as conn:
            for entry in data:
                insert_query = text("""
                    INSERT INTO search_data (term, incidence, site, timestamp)
                    VALUES (:term, :incidence, :site, :timestamp)
                """)
                conn.execute(insert_query, {
                    'term': entry['term'],
                    'incidence': entry['incidence'],
                    'site': entry['site'],
                    'timestamp': entry['timestamp']
                })
    except Exception as e:
        logging.error(f"Database insert failed: {e}")

def main():
    print("DAG WORKS!")
    all_results = []

    for url, site_name in urls.items():
        results = count_keywords_in_headings(url, keywords, site_name)
        if results:
            all_results.extend(results)

    if all_results:
        insert_data(all_results)
        logging.info("Data inserted successfully!")
    else:
        logging.info("No data to insert.")

if __name__ == '__main__':
    main()
