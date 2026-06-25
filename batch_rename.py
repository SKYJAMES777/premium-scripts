#!/usr/bin/env python3
"""Batch File Renamer - Rename files by pattern matching.
Price: $10"""
import os, re, sys
def rename(directory, pattern, replacement, dry_run=True):
    count = 0
    for fn in os.listdir(directory):
        new_name = re.sub(pattern, replacement, fn)
        if new_name != fn:
            if not dry_run: os.rename(os.path.join(directory,fn), os.path.join(directory,new_name))
            print("%s -> %s%s" % (fn, new_name, " (dry)" if dry_run else ""))
            count += 1
    print("%d files renamed" % count)
if __name__ == "__main__":
    dry = "--dry" in sys.argv or "-n" in sys.argv
    rename(sys.argv[1], sys.argv[2], sys.argv[3], dry_run=dry) if len(sys.argv)>3 else print("Usage: python batch_rename.py <dir> <pattern> <replacement> [--dry]")
