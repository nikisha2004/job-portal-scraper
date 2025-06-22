import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class IndeedScraper:
    def __init__(self, query="python developer", location="India"):
        self.query, self.location = query, location
        self.source = "Indeed"
        self.base_url = "https://www.indeed.com/jobs?q={}&l={}&start={}"

    def scrape_jobs(self):
        jobs, seen = [], set()
        start, max_jobs = 0, 1000

        while len(jobs) < max_jobs:
            url = self.base_url.format(self.query.replace(" ", "+"), self.location.replace(" ", "+"), start)
            logging.info(f"Indeed → loading start={start}: {url}")
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select("a.tapItem")

            if not cards:
                logging.info("No jobs found on Indeed, finishing.")
                break

            for c in cards:
                if len(jobs) >= max_jobs: break
                t = c.select_one("h2.jobTitle span")
                comp = c.select_one("span.companyName")
                loc = c.select_one("div.companyLocation")
                link = c.get("href")
                if not (t and link): continue
                url_job = link if link.startswith("http") else urljoin("https://www.indeed.com", link)
                if url_job in seen: continue
                seen.add(url_job)
                jobs.append({
                    "title": t.text.strip(),
                    "company": comp.text.strip() if comp else "",
                    "location": loc.text.strip() if loc else "",
                    "summary": "",
                    "url": url_job,
                    "source": self.source
                })

            logging.info(f"Indeed → collected {len(jobs)} jobs so far")
            start += 10
            time.sleep(1)

        return jobs
