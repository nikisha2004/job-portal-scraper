# shine.py
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ShineScraper:
    def __init__(self, query="python developer", location="India"):
        self.query = query
        self.location = location
        self.source = "Shine"
        self.base_url = "https://www.shine.com/job-search/{}-jobs-in-{}-{}/"

    def scrape_jobs(self):
        jobs = []
        seen_urls = set()
        page = 1
        max_jobs = 1000

        while len(jobs) < max_jobs:
            search_url = self.base_url.format(
                self.query.replace(" ", "-"),
                self.location.replace(" ", "-"),
                page
            )
            logging.info(f"Shine → Loading page {page}: {search_url}")

            try:
                response = requests.get(search_url, timeout=10)
                if response.status_code != 200:
                    logging.warning(f"Shine page {page} returned status {response.status_code}")
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                job_cards = soup.select("li.jobCard_jobCard__jjUmu")

                if not job_cards:
                    logging.info("No more job cards found on Shine. Stopping.")
                    break

                for card in job_cards:
                    if len(jobs) >= max_jobs:
                        break

                    title_elem = card.select_one("h2 a")
                    company_elem = card.select_one("span.jobCard_compName__m3Uj5")
                    location_elem = card.select_one("li.jobCard_locationIcon__zrWt2 span")

                    title = title_elem.text.strip() if title_elem else "N/A"
                    company = company_elem.text.strip() if company_elem else "N/A"
                    location = location_elem.text.strip() if location_elem else "N/A"

                    job_url = title_elem["href"] if title_elem and title_elem.has_attr("href") else ""
                    if job_url.startswith("/"):
                        job_url = urljoin("https://www.shine.com", job_url)

                    if job_url in seen_urls:
                        continue
                    seen_urls.add(job_url)

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "summary": "",
                        "url": job_url,
                        "source": self.source
                    })

                logging.info(f"Shine → Collected {len(jobs)} jobs so far")
                page += 1
                time.sleep(1)

            except Exception as e:
                logging.error(f"Shine → Error scraping page {page}: {e}")
                break

        return jobs
