import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_trustpilot_reviews(url, num_pages=5, output_file="southwest-review-analysis/data/raw_reviews/southwest_reviews.csv"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    all_reviews = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}?page={page}"
        print(f"Scraping {page_url}...")
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('p', {"data-service-review-text-typography": "true"})
        
        for review in reviews:
            text = review.get_text(strip=True)
            if text:
                all_reviews.append([text])

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save reviews to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Review"])  # header
        writer.writerows(all_reviews)

    print(f"Scraped {len(all_reviews)} reviews. Saved to {output_file}.")

if __name__ == "__main__":
    # Southwest Airlines on Trustpilot:
    trustpilot_url = "https://www.trustpilot.com/review/www.southwest.com"
    scrape_trustpilot_reviews(trustpilot_url)