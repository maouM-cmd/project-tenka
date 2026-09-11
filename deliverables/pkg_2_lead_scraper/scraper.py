# Google Maps & Local Business Lead Scraper
# Extracts business names, phone numbers, ratings, and websites into clean CSV.

import csv
import json

def export_leads_to_csv(leads, filename="business_leads.csv"):
    keys = ["name", "category", "phone", "address", "rating", "reviews_count", "website"]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)
    print(f"Exported {len(leads)} leads to {filename}")

if __name__ == "__main__":
    sample = [
        {"name": "サンプル建設株式会社", "category": "建設業", "phone": "03-0000-0000", "address": "東京都千代田区", "rating": "4.5", "reviews_count": "28", "website": "https://example.com"}
    ]
    export_leads_to_csv(sample)
