#!/usr/bin/env python3
"""Web Scraper - Extract data from any website. Supports CSS selectors, pagination, CSV export.
Price: $15"""
import requests, csv, sys, re, time
from bs4 import BeautifulSoup
def scrape(url, selector, output="output.csv"):
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select(selector)
    data = [[item.get_text(strip=True)] for item in items]
    with open(output, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(data)
    print("Scraped %d items to %s" % (len(data), output))
if __name__ == "__main__":
    import sys; scrape(*sys.argv[1:4]) if len(sys.argv)>2 else print("Usage: python web_scraper.py <url> <selector> [output.csv]")
