#!/usr/bin/env python3
"""批量文件重命名/整理器 - 可出售"""
import os, re, hashlib, argparse
from datetime import datetime

def rename_files(directory, pattern, dry_run=True):
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            name, ext = os.path.splitext(f)
            new_name = pattern.replace('{name}', name).replace('{ext}', ext).replace('{date}', datetime.now().strftime('%Y%m%d'))
            new_name = re.sub(r'[<>:"/\\|?*]', '_', new_name)
            if dry_run:
                print(f'[DRY] {f} -> {new_name}')
            else:
                os.rename(os.path.join(directory, f), os.path.join(directory, new_name))
                print(f'OK: {f} -> {new_name}')

def dedup_by_hash(directory, dry_run=True):
    seen = {}
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isfile(path):
            h = hashlib.md5(open(path, 'rb').read()).hexdigest()
            if h in seen:
                if dry_run: print(f'[DRY] DUPLICATE: {f} (same as {seen[h]})')
                else: os.remove(path); print(f'DELETED: {f}')
            else: seen[h] = f
    print(f'Found {len(seen)} unique files')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='文件批量整理工具')
    p.add_argument('cmd', choices=['rename','dedup'])
    p.add_argument('-d','--dir', default='.')
    p.add_argument('-p','--pattern', default='{name}{ext}')
    p.add_argument('--exec', action='store_true', help='Actually run (default: dry run)')
    a = p.parse_args()
    if a.cmd == 'rename': rename_files(a.dir, a.pattern, not a.exec)
    elif a.cmd == 'dedup': dedup_by_hash(a.dir, not a.exec)
