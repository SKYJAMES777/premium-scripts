#!/usr/bin/env python3
"""PDF Generator - Create PDFs from text/HTML templates.
Price: $18"""
from fpdf import FPDF
import sys
def generate(text_file, output="output.pdf"):
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", size=12)
    with open(text_file) as f:
        for line in f: pdf.cell(200, 10, txt=line.strip(), ln=True)
    pdf.output(output)
    print("PDF saved to %s" % output)
if __name__ == "__main__":
    generate(sys.argv[1]) if len(sys.argv)>1 else print("Usage: python pdf_generator.py <text.txt> [output.pdf]")
