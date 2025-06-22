# database.py
import mysql.connector
import logging
import csv
import pandas as pd
import re

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",  # ✅ Update this if needed
            database="jobs_db"
        )
        self.cursor = self.connection.cursor()
        logging.info("Successfully connected to MySQL database")

    @staticmethod
    def normalize(text):
        """Normalize text for deduplication (lowercase, strip spaces, remove special chars)."""
        if not text:
            return ""
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s]", "", text)
        return text.strip().lower()

    def count_jobs(self):
        self.cursor.execute("SELECT COUNT(*) FROM jobs")
        return self.cursor.fetchone()[0]

    def get_all_jobs(self):
        self.cursor.execute("SELECT title, company, location, summary, url, source FROM jobs")
        return self.cursor.fetchall()

    def export_to_csv(self, filename):
        jobs = self.get_all_jobs()
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Company', 'Location', 'Summary', 'URL', 'Source'])
            writer.writerows(jobs)
        logging.info(f"Exported data to {filename}")

    def export_to_excel(self, filename):
        jobs = self.get_all_jobs()
        df = pd.DataFrame(jobs, columns=['Title', 'Company', 'Location', 'Summary', 'URL', 'Source'])
        df.to_excel(filename, index=False)
        logging.info(f"Exported data to {filename}")

    def insert_jobs(self, jobs):
        for job in jobs:
            try:
                # Normalize fields
                title = self.normalize(job.get("title", ""))
                company = self.normalize(job.get("company", ""))
                location = job.get("location", "").strip()
                summary = job.get("summary", "").strip()
                url = job.get("url", "").strip()
                source = job.get("source", "").strip()

                # SQL Insert with ON DUPLICATE KEY UPDATE
                query = """
                INSERT INTO jobs (title, company, location, summary, url, source)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    summary = VALUES(summary),
                    url = VALUES(url),
                    location = VALUES(location)
                """
                self.cursor.execute(query, (title, company, location, summary, url, source))
                self.connection.commit()
            except Exception as e:
                logging.warning(f"Failed to insert job: {e}")
