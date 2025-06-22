import pandas as pd
from database import Database

def export_to_csv(filename="jobs.csv"):
    db = Database()
    jobs = db.fetch_all_jobs()
    df = pd.DataFrame(jobs, columns=[
        "id", "title", "company", "location", "experience", "summary", "url", "source"
    ])
    df.to_csv(filename, index=False)
    print(f"✅ Exported to CSV: {filename}")

def export_to_excel(filename="jobs.xlsx"):
    db = Database()
    jobs = db.fetch_all_jobs()
    df = pd.DataFrame(jobs, columns=[
        "id", "title", "company", "location", "experience", "summary", "url", "source"
    ])
    df.to_excel(filename, index=False)
    print(f"✅ Exported to Excel: {filename}")
