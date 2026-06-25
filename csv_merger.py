#!/usr/bin/env python3
"""CSV Merger - Combine multiple CSV files with same headers.
Price: $10"""
import csv, sys, glob
def merge(pattern, output="merged.csv"):
    headers = None; rows = []
    for fn in glob.glob(pattern):
        with open(fn) as f:
            reader = csv.reader(f)
            h = next(reader)
            if headers is None: headers = h
            rows.extend(row for row in reader)
    with open(output, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(rows)
    print("Merged %d files -> %d rows" % (len(glob.glob(pattern)), len(rows)))
if __name__ == "__main__":
    merge(sys.argv[1]) if len(sys.argv)>1 else print("Usage: python csv_merger.py <glob_pattern> [merged.csv]")
