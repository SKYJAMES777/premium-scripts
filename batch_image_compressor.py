#!/usr/bin/env python3
"""批量图片压缩工具 - 支持JPEG/PNG/WebP，可设置压缩质量"""
import os, sys, argparse
from PIL import Image

SUPPORTED = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')

def compress_image(input_path, output_path, quality=85, max_width=None):
    img = Image.open(input_path)
    if img.mode == 'RGBA':
        img = img.convert('RGBA')
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    if max_width and img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    
    ext = os.path.splitext(output_path)[1].lower()
    if ext in ('.jpg', '.jpeg'):
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
    elif ext == '.png':
        img.save(output_path, 'PNG', optimize=True)
    elif ext == '.webp':
        img.save(output_path, 'WEBP', quality=quality)
    else:
        img.save(output_path)
    
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    ratio = (1 - compressed_size / original_size) * 100
    return original_size, compressed_size, ratio

def batch_compress(input_dir, output_dir, quality=85, max_width=None, recursive=False):
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(SUPPORTED):
                in_path = os.path.join(root, f)
                rel = os.path.relpath(root, input_dir)
                out_dir = os.path.join(output_dir, rel)
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, f)
                
                try:
                    orig, comp, ratio = compress_image(in_path, out_path, quality, max_width)
                    results.append((f, orig, comp, ratio))
                    print(f"  ✓ {f}: {orig//1024}KB → {comp//1024}KB ({ratio:.1f}%)")
                except Exception as e:
                    print(f"  ✗ {f}: {e}")
        
        if not recursive:
            break
    
    if results:
        total_orig = sum(r[1] for r in results)
        total_comp = sum(r[2] for r in results)
        total_ratio = (1 - total_comp / total_orig) * 100
        print(f"\n总计: {len(results)} 个文件, {total_orig//1024}KB → {total_comp//1024}KB (节省 {total_ratio:.1f}%)")
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='批量图片压缩工具')
    parser.add_argument('input', help='输入目录或文件')
    parser.add_argument('-o', '--output', default='compressed', help='输出目录')
    parser.add_argument('-q', '--quality', type=int, default=85, help='压缩质量 1-100')
    parser.add_argument('--max-width', type=int, help='最大宽度(像素)')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        out_path = os.path.join(args.output, os.path.basename(args.input))
        os.makedirs(args.output, exist_ok=True)
        orig, comp, ratio = compress_image(args.input, out_path, args.quality, args.max_width)
        print(f"{os.path.basename(args.input)}: {orig//1024}KB → {comp//1024}KB ({ratio:.1f}%)")
    else:
        batch_compress(args.input, args.output, args.quality, args.max_width, args.recursive)
