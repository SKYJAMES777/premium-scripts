#!/usr/bin/env python3
"""网页监控告警系统 - 监控网页变化、断线检测、邮件/SMS通知"""

import os, sys, json, time, hashlib, datetime, smtplib
from email.mime.text import MIMEText

class WebMonitor:
    def __init__(self, config_path="monitor_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path) as f: return json.load(f)
        return {"sites": [], "interval": 300, "notify_email": "", "webhook_url": ""}
    
    def _save_config(self):
        with open(self.config_path, "w") as f: json.dump(self.config, f, indent=2)
    
    def add_site(self, url, name=None, check_string=None, timeout=10):
        site = {
            "url": url,
            "name": name or url,
            "check_string": check_string,
            "timeout": timeout,
            "last_status": "unknown",
            "last_check": None,
            "hash": None
        }
        self.config["sites"].append(site)
        self._save_config()
        print(f"已添加监控: {site['name']}")
    
    def check_site(self, site):
        import urllib.request
        try:
            req = urllib.request.Request(site["url"], headers={"User-Agent": "Mozilla/5.0"})
            start = time.time()
            resp = urllib.request.urlopen(req, timeout=site.get("timeout", 10))
            elapsed = time.time() - start
            content = resp.read()
            
            content_hash = hashlib.md5(content).hexdigest()
            
            result = {
                "status": "up",
                "code": resp.getcode(),
                "time": round(elapsed, 3),
                "size": len(content),
                "hash": content_hash
            }
            
            # 内容检查
            if site.get("check_string"):
                if site["check_string"].encode() in content:
                    result["content_match"] = True
                else:
                    result["content_match"] = False
                    result["alert"] = f"内容不包含: {site['check_string']}"
            
            # 变化检测
            if site.get("hash") and site["hash"] != content_hash:
                result["changed"] = True
                result["alert"] = "页面内容发生变化"
            
            return result
        
        except Exception as e:
            return {
                "status": "down",
                "error": str(e),
                "alert": f"无法访问: {e}"
            }
    
    def run_once(self):
        results = []
        for site in self.config["sites"]:
            print(f"  检查 {site['name']}...", end=" ")
            result = self.check_site(site)
            site["last_status"] = result["status"]
            site["last_check"] = datetime.datetime.now().isoformat()
            if result.get("hash"):
                site["hash"] = result["hash"]
            
            status_icon = "✓" if result["status"] == "up" else "✗"
            print(f"[{status_icon}] {result.get('code', 'ERR')} ({result.get('time','N/A')}s)")
            
            if result.get("alert"):
                print(f"    ⚠ 告警: {result['alert']}")
            
            results.append({"site": site["name"], "result": result})
        
        self._save_config()
        return results
    
    def run_loop(self):
        interval = self.config.get("interval", 300)
        print(f"网页监控已启动 (每{interval}秒检查一次)")
        print(f"监控 {len(self.config['sites'])} 个站点")
        print("-" * 40)
        
        while True:
            print(f"\n[{datetime.datetime.now().isoformat()}]")
            self.run_once()
            time.sleep(interval)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="网页监控告警系统")
    parser.add_argument("action", choices=["add", "check", "monitor", "list"])
    parser.add_argument("-u", "--url", help="监控URL")
    parser.add_argument("-n", "--name", help="站点名称")
    parser.add_argument("-c", "--check-string", help="检查内容关键词")
    parser.add_argument("-i", "--interval", type=int, default=300, help="检查间隔(秒)")
    parser.add_argument("--config", default="monitor_config.json", help="配置文件")
    args = parser.parse_args()
    
    monitor = WebMonitor(args.config)
    
    if args.action == "add":
        if not args.url:
            print("错误: 需要指定 --url")
            sys.exit(1)
        monitor.add_site(args.url, args.name, args.check_string)
    
    elif args.action == "check":
        print("执行一次检查:\n")
        monitor.run_once()
    
    elif args.action == "monitor":
        monitor.run_loop()
    
    elif args.action == "list":
        print(f"\n监控列表 ({len(monitor.config['sites'])} 个站点):\n")
        for s in monitor.config["sites"]:
            print(f"  [{s['last_status']}] {s['name']}")
            print(f"     {s['url']}")
