#!/usr/bin/env python3
"""QR Code Generator - Generate QR codes from text/URLs.
Price: $8"""
import qrcode, sys
def generate(data, output="qr.png"):
    img = qrcode.make(data)
    img.save(output)
    print("QR code saved to %s" % output)
if __name__ == "__main__":
    generate(sys.argv[1]) if len(sys.argv)>1 else print("Usage: python qr_generator.py <data> [output.png]")
