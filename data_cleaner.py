#!/usr/bin/env python3
"""Data Cleaner - Remove duplicates, format columns, handle missing values.
Price: $15"""
import csv, sys
def clean(input_file, output="cleaned.csv"):
    rows = []
    with open(input_file) as f:
        reader = csv.reader(f)
        for row in reader:
            row = [c.strip() for c in row]
            if any(c for c in row): rows.append(row)
    seen = set(); unique = []
    for row in rows:
        key = tuple(row)
        if key not in seen: seen.add(key); unique.append(row)
    with open(output, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(unique)
    print("Cleaned: %d -> %d rows" % (len(rows), len(unique)))
if __name__ == "__main__":
    clean(sys.argv[1]) if len(sys.argv)>1 else print("Usage: python data_cleaner.py <input.csv>")
