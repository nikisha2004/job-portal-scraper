import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

class NaukriScraper:
    def __init__(self, query="python developer", location="India"):
        self.query = query
        self.location = location
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://www.naukri.com/{}-jobs-in-{}?k={}&l={}&pageNo={}"
        self.source = "Naukri"

    def scrape_jobs(self):
        jobs = []
        seen_urls = set()
        max_jobs = 1000
        page = 1

        while len(jobs) < max_jobs and page <= 50:
            url = self.base_url.format(
                self.query.replace(" ", "-"),
                self.location.replace(" ", "-"),
                self.query.replace(" ", "%20"),
                self.location.replace(" ", "%20"),
                page
            )
            logging.info(f"Scraping page {page}: {url}")
            self.driver.get(url)
            time.sleep(5)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            job_cards = soup.select("div.srp-jobtuple-wrapper")

            if not job_cards:
                logging.info("No job cards found on page. Stopping.")
                break

            for card in job_cards:
                if len(jobs) >= max_jobs:
                    break
                try:
                    title_elem = card.select_one("a.title")
                    company_elem = card.select_one("a.subTitle")
                    location_elem = card.select_one("li.location span")

                    title = title_elem.text.strip() if title_elem else "N/A"
                    company = company_elem.text.strip() if company_elem else "N/A"
                    location = location_elem.text.strip() if location_elem else "N/A"

                    job_url = title_elem["href"] if title_elem and title_elem.has_attr("href") else ""
                    if job_url.startswith("/"):
                        job_url = urljoin("https://www.naukri.com", job_url)

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
                except Exception as e:
                    logging.warning(f"Error parsing job card: {e}")

            logging.info(f"Page {page} done. Collected {len(jobs)} jobs so far.")
            page += 1
            time.sleep(3)

        self.driver.quit()
        return jobs
