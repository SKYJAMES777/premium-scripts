#!/usr/bin/env python3
"""Batch Image Resizer - Resize/compress images in bulk.
Price: $12"""
from PIL import Image
import os, sys
def resize_dir(input_dir, output_dir, width=800):
    os.makedirs(output_dir, exist_ok=True)
    for fn in os.listdir(input_dir):
        if fn.lower().endswith((".jpg",".png",".jpeg")):
            img = Image.open(os.path.join(input_dir, fn))
            ratio = width / img.width
            img.resize((width, int(img.height*ratio))).save(os.path.join(output_dir, fn))
            print("Resized %s" % fn)
if __name__ == "__main__":
    resize_dir(*sys.argv[1:4]) if len(sys.argv)>2 else print("Usage: python image_resizer.py <input_dir> <output_dir> [width=800]")
