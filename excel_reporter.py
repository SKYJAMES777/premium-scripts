#!/usr/bin/env python3
"""Excel Report Generator - Create formatted Excel reports from CSV/JSON data.
Price: $20"""
import openpyxl, json, csv, sys
def generate(input_file, output="report.xlsx"):
    wb = openpyxl.Workbook(); ws = wb.active
    if input_file.endswith(".csv"):
        with open(input_file) as f:
            for row in csv.reader(f): ws.append(row)
    elif input_file.endswith(".json"):
        data = json.load(open(input_file))
        if data: ws.append(list(data[0].keys()))
        for item in data: ws.append(list(item.values()))
    wb.save(output)
    print("Report saved to %s" % output)
if __name__ == "__main__":
    generate(sys.argv[1]) if len(sys.argv)>1 else print("Usage: python excel_reporter.py <input.csv|json>")
