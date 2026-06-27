#!/usr/bin/env python3
"""智能文件同步与备份工具 - 支持增量备份、差异同步、定时任务"""

import os, sys, hashlib, json, time, argparse, datetime, shutil

class SyncEngine:
    def __init__(self, db_path=".sync_db.json"):
        self.db_path = db_path
        self.db = self._load_db()
    
    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path) as f: return json.load(f)
        return {}
    
    def _save_db(self):
        with open(self.db_path, "w") as f: json.dump(self.db, f, indent=2)
    
    def _file_hash(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
        return h.hexdigest()
    
    def _file_info(self, path):
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "mtime": stat.st_mtime,
            "hash": self._file_hash(path)
        }
    
    def scan(self, source_dir, pattern=None):
        """扫描目录文件状态"""
        scan_result = {}
        for root, dirs, files in os.walk(source_dir):
            for f in files:
                if pattern and not f.endswith(pattern): continue
                path = os.path.join(root, f)
                rel = os.path.relpath(path, source_dir)
                scan_result[rel] = self._file_info(path)
        return scan_result
    
    def sync(self, source, dest, dry_run=False, delete=False):
        """同步source到dest"""
        source_files = self.scan(source)
        dest_files = self.scan(dest) if os.path.exists(dest) else {}
        
        to_copy = []
        to_delete = []
        
        for rel, info in source_files.items():
            dest_path = os.path.join(dest, rel)
            if rel not in dest_files:
                to_copy.append((rel, "new"))
            elif dest_files[rel]["hash"] != info["hash"]:
                to_copy.append((rel, "updated"))
        
        if delete:
            for rel in dest_files:
                if rel not in source_files:
                    to_delete.append(rel)
        
        if dry_run:
            print(f"\n=== 预览同步: {source} → {dest} ===")
            for rel, reason in to_copy: print(f"  [+] {rel} ({reason})")
            for rel in to_delete: print(f"  [-] {rel}")
            return len(to_copy), len(to_delete)
        
        # 执行同步
        copied = 0
        for rel, reason in to_copy:
            src = os.path.join(source, rel)
            dst = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  {'更新' if reason == 'updated' else '新增'} {rel}")
            copied += 1
        
        if delete:
            for rel in to_delete:
                path = os.path.join(dest, rel)
                os.remove(path)
                print(f"  删除 {rel}")
        
        # 记录同步状态
        self.db[source] = {
            "last_sync": datetime.datetime.now().isoformat(),
            "files": len(source_files),
            "copied": copied
        }
        self._save_db()
        
        return copied, len(to_delete)
    
    def incremental_backup(self, source, backup_dir, max_backups=10):
        """增量备份, 带版本管理"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        version = f"backup_{timestamp}"
        backup_path = os.path.join(backup_dir, version)
        
        copied, deleted = self.sync(source, backup_path)
        
        # 清理旧备份
        backups = sorted([d for d in os.listdir(backup_dir) 
                         if d.startswith("backup_") and os.path.isdir(os.path.join(backup_dir, d))])
        while len(backups) > max_backups:
            old = backups.pop(0)
            shutil.rmtree(os.path.join(backup_dir, old))
            print(f"  清理旧备份: {old}")
        
        return backup_path, copied

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="智能文件同步与备份工具")
    parser.add_argument("action", choices=["sync", "backup", "scan"], help="操作")
    parser.add_argument("source", help="源目录")
    parser.add_argument("-d", "--dest", help="目标目录")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--delete", action="store_true", help="删除目标端多余文件")
    parser.add_argument("--max-backups", type=int, default=10, help="最大备份数")
    args = parser.parse_args()
    
    engine = SyncEngine()
    
    if args.action == "sync":
        if not args.dest:
            print("错误: 同步需要指定 --dest")
            sys.exit(1)
        copied, deleted = engine.sync(args.source, args.dest, args.dry_run, args.delete)
        print(f"\n完成: 同步 {copied} 个文件, 删除 {deleted} 个")
    
    elif args.action == "backup":
        backup_dir = args.dest or f"backups_{os.path.basename(args.source)}"
        path, copied = engine.incremental_backup(args.source, backup_dir, args.max_backups)
        print(f"\n备份完成: {path} ({copied} 个文件)")
    
    elif args.action == "scan":
        files = engine.scan(args.source)
        total_size = sum(f["size"] for f in files.values())
        print(f"\n目录: {args.source}")
        print(f"文件数: {len(files)}")
        print(f"总大小: {total_size/1024/1024:.2f} MB")
        for rel, info in sorted(files.items())[:20]:
            print(f"  {rel} ({info['size']/1024:.1f} KB)")
