MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'job_portal',
    'raise_on_warnings': True
}

# Job portals to scrape
PORTALS = ['indeed', 'naukri', 'shine']

# Rate limiting (requests per minute)
RATE_LIMIT = {
    'indeed': 30,
    'naukri': 30,
    'shine': 30
}

# User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
