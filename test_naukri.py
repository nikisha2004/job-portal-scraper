from scraper.naukri import NaukriScraper

def test_naukri_fetches_results():
    scraper = NaukriScraper("Python Developer", "Remote")
    jobs = scraper.scrape_jobs()
    assert len(jobs) > 0