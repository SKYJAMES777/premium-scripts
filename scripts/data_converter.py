#!/usr/bin/env python3
"""CSV/Excel数据清洗和格式转换工具 - 可出售"""
import csv, json, os, argparse
from datetime import datetime

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f'Converted {len(rows)} rows: {csv_file} -> {json_file}')

def clean_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [r for r in reader if any(c.strip() for c in r)]
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f'Cleaned {input_file}: removed {sum(1 for _ in open(input_file))-len(rows)} empty rows')

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data: return print('Empty JSON')
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f'Converted {len(data)} records: {json_file} -> {csv_file}')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='数据格式转换工具')
    p.add_argument('cmd', choices=['csv2json','clean','json2csv'])
    p.add_argument('-i','--input', required=True)
    p.add_argument('-o','--output')
    a = p.parse_args()
    out = a.output or (a.input.rsplit('.',1)[0] + ('_out.csv' if a.cmd=='csv2json' else '_out.json'))
    if a.cmd == 'csv2json': csv_to_json(a.input, out)
    elif a.cmd == 'clean': clean_csv(a.input, out)
    elif a.cmd == 'json2csv': json_to_csv(a.input, out)
