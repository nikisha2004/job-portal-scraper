# 📄 README.md

# 🛠️ Job Scraper Project

This is a Python-based job scraper that uses Selenium to collect job listings from Naukri, Shine, and Indeed and stores them in a MySQL database with deduplication support.

## 📌 Features

* Scrapes job listings for a specific role and location.
* Currently supports:

  * Naukri.com
  * Shine.com
  * Indeed.com
* Stores scraped data in a MySQL database.
* Automatically avoids duplicate entries based on job title and company.
* Easy to run without command-line arguments (can be customized).
* Can be extended to other platforms.

## 🧰 Tech Stack

* Python 3.10+
* Selenium & undetected-chromedriver
* WebDriver Manager
* MySQL


## ⚙️ Setup Instructions

1. ✅ Clone the repository or download the files

2. ✅ Install required Python packages:

```bash
pip install -r requirements.txt
```

Here’s a sample requirements.txt:

```txt
selenium
undetected-chromedriver
webdriver-manager
mysql-connector-python
```

3. ✅ Configure your MySQL database

Make sure your database is running and a table exists:

```sql
CREATE DATABASE IF NOT EXISTS job_scraper;
USE job_scraper;

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    experience TEXT,
    summary TEXT,
    url TEXT,
    source TEXT,
    UNIQUE KEY unique_job (title(255), company(255))
);
```

Update your database credentials in database.py:

```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="job_scraper"
)
```

## 🚀 How to Run

From your project directory:

```bash
python main.py
```

You’ll be prompted to enter:

* 🔎 Job title (e.g., ACCA Accountant)
* 📍 Location (e.g., India)

The scraper will run, extract jobs from all platforms, and store them in the database.

## 📝 Example Output (in Database)

| ID | Title            | Company  | Location | Summary              | URL          | Source |
| -- | ---------------- | -------- | -------- | -------------------- | ------------ | ------ |
| 1  | Python Developer | ABC Corp | Remote   | Great opportunity... | https\://... | Naukri |

## 📦 Folder Structure

```
scraper/
│
├── main.py               # Entry point
├── database.py           # MySQL handler
├── naukri.py             # Naukri scraper
├── shine.py              # Shine scraper
├── indeed.py             # Indeed scraper
└── README.md             # Project guide

#🧹 Data Deduplication

Uses MySQL UNIQUE constraint (title, company) to prevent duplicate entries.

Filters out NULL/empty entries before insertion.

#🧪 Testing

Located in /test/ folder.

Includes one test per portal and one end-to-end test.