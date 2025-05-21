import requests
from bs4 import BeautifulSoup
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  # updated import

base_url = "https://uidai.gov.in"
faq_sidebar_page = "https://uidai.gov.in/en/contact-support/have-any-question/297-english-uk/faqs/enrolment-update/aadhaar-updation.html"
headers = {"User-Agent": "Mozilla/5.0"}

# Setup session with retry strategy
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,               # exponential backoff: 2s, 4s, 8s, ...
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

# Step 1: Get the sidebar FAQ topic links from an inner FAQ page
response = session.get(faq_sidebar_page, headers=headers, timeout=40)
soup = BeautifulSoup(response.content, "html.parser")

# FIXED: Get all <a> tags with href containing "/faqs/" from the sidebar
faq_links = soup.select('#sidebarRight a[href*="/faqs/"]')
faq_paths = list({a['href'].strip() for a in faq_links if a['href'].startswith("/")})

print(f"✅ Found {len(faq_paths)} FAQ topic URLs")

# Step 2: Scrape each topic page
faq_data = []

for path in faq_paths:
    url = base_url + path
    try:
        response = session.get(url, headers=headers, timeout=40)
        page_soup = BeautifulSoup(response.content, "html.parser")

        panels = page_soup.select(".js-accordion_container .panel")
        print(f"🔍 Scraping {url} — {len(panels)} FAQs found")

        for panel in panels:
            question_div = panel.select_one(".accordion_head")
            answer_div = panel.select_one(".accordion_body .accordion-content-inner")

            if question_div and answer_div:
                question = question_div.get_text(strip=True)
                answer = answer_div.get_text(separator=" ", strip=True)
                faq_data.append((question, answer, url))

        time.sleep(2)  # Respect rate limits

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

# Save to TXT
with open("all_aadhaar_faqs.txt", "w", encoding="utf-8") as f:
    for idx, (q, a, url) in enumerate(faq_data, 1):
        f.write(f"Q{idx}: {q}\nA{idx}: {a}\nSource: {url}\n\n")

# Save to CSV
with open("all_aadhaar_faqs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Question", "Answer", "Source URL"])
    writer.writerows(faq_data)

print(f"\n✅ Scraped {len(faq_data)} total FAQs from {len(faq_paths)} topics.")
print("📁 Saved to 'all_aadhaar_faqs.txt' and 'all_aadhaar_faqs.csv'")
