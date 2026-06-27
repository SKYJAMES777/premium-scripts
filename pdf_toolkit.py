#!/usr/bin/env python3
"""批量PDF合并/分割/水印工具 - 可出售"""
import os, argparse
from PyPDF2 import PdfReader, PdfMerger, PdfWriter

def merge_pdfs(input_files, output):
    merger = PdfMerger()
    for f in input_files:
        merger.append(f)
    merger.write(output)
    merger.close()
    print(f'Merged {len(input_files)} PDFs into {output}')

def split_pdf(input_file, output_dir):
    reader = PdfReader(input_file)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out = os.path.join(output_dir, f'page_{i+1}.pdf')
        with open(out, 'wb') as f:
            writer.write(f)
    print(f'Split {len(reader.pages)} pages to {output_dir}')

def add_watermark(input_file, watermark_text, output):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(reader.pages[0])
        writer.add_page(page)
    with open(output, 'wb') as f:
        writer.write(f)
    print(f'Watermark added to {output}')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='PDF 工具集')
    p.add_argument('cmd', choices=['merge','split','watermark'])
    p.add_argument('-i','--input', nargs='+')
    p.add_argument('-o','--output', default='output.pdf')
    p.add_argument('-d','--dir', default='./split')
    a = p.parse_args()
    if a.cmd == 'merge': merge_pdfs(a.input, a.output)
    elif a.cmd == 'split': split_pdf(a.input[0], a.dir)
    elif a.cmd == 'watermark': add_watermark(a.input[0], 'WATERMARK', a.output)
