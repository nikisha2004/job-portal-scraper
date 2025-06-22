# main.py
import logging
from database import Database
from naukri import NaukriScraper
from shine import ShineScraper
from indeed import IndeedScraper

def main():
    logging.basicConfig(level=logging.INFO)
    db = Database()

    search_term = "python developer"
    location = "India"

    all_jobs = []

    for Scraper, name in [(NaukriScraper, "Naukri"), (ShineScraper, "Shine"), (IndeedScraper, "Indeed")]:
        logging.info(f"Scraping {name}")
        try:
            scraper = Scraper(search_term, location)
            jobs = scraper.scrape_jobs()
            logging.info(f"Found {len(jobs)} jobs from {name}")
            db.insert_jobs(jobs)
            all_jobs.extend(jobs)
        except Exception as e:
            logging.error(f"{name} scraping error: {e}")

    total = db.count_jobs()
    logging.info(f"Total jobs in database: {total}")

    # Export to files
    db.export_to_csv("exported_jobs.csv")
    db.export_to_excel("exported_jobs.xlsx")
    logging.info("Export completed: 'exported_jobs.csv' and 'exported_jobs.xlsx'")

if __name__ == "__main__":
    main()
