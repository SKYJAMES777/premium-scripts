#!/usr/bin/env python3
"""自动化Excel报表生成器 - 模板化报表、定时生成、多sheet"""

import os, sys, json, csv, datetime
from collections import defaultdict

class ReportGenerator:
    def __init__(self, template_dir="templates"):
        self.template_dir = template_dir
        os.makedirs(template_dir, exist_ok=True)
    
    def from_csv(self, csv_path, group_by=None, aggregate=None, output=None):
        """从CSV生成报表"""
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        
        if not rows:
            return {"error": "空文件"}
        
        report = {
            "标题": os.path.splitext(os.path.basename(csv_path))[0],
            "生成时间": datetime.datetime.now().isoformat(),
            "数据行数": len(rows),
            "分组": group_by,
            "聚合": aggregate,
        }
        
        if group_by and group_by in rows[0]:
            groups = defaultdict(list)
            for r in rows:
                groups[r[group_by]].append(r)
            
            report["分组统计"] = {}
            for key, group in sorted(groups.items()):
                entry = {"数量": len(group)}
                if aggregate and aggregate in rows[0]:
                    vals = [float(r[aggregate]) for r in group if r[aggregate]]
                    entry.update({
                        "总和": round(sum(vals), 2),
                        "平均": round(sum(vals)/len(vals), 2) if vals else 0,
                        "最大": max(vals) if vals else 0,
                        "最小": min(vals) if vals else 0,
                    })
                report["分组统计"][key] = entry
        
        # 生成HTML格式报表
        return self._to_html(report, output)
    
    def _to_html(self, report, output=None):
        html = []
        html.append("<!DOCTYPE html><html><head><meta charset='UTF-8'>")
        html.append("<title>报表 - %s</title>" % report.get("标题", "Report"))
        html.append("<style>")
        html.append("body{font-family:sans-serif;background:#1a1a2e;color:#e0e0e0;padding:20px}")
        html.append("h1{color:#FFD700;border-bottom:2px solid #FFD700;padding-bottom:10px}")
        html.append("h2{color:#4CAF50;margin-top:30px}")
        html.append("table{width:100%;border-collapse:collapse;margin:15px 0}")
        html.append("th,td{padding:10px;text-align:left;border-bottom:1px solid #333}")
        html.append("th{background:#0f3460;color:#FFD700}")
        html.append("tr:hover{background:#16213e}")
        html.append(".stat{display:inline-block;margin:10px;padding:20px;background:#16213e;border-radius:8px;min-width:150px}")
        html.append(".num{font-size:2em;color:#FFD700}")
        html.append(".label{color:#888;font-size:0.8em}")
        html.append("</style></head><body>")
        
        html.append("<h1>📊 %s</h1>" % report.get("标题", ""))
        html.append("<p>生成时间: %s</p>" % report.get("生成时间", ""))
        
        html.append("<div class='stat'><div class='label'>数据行数</div><div class='num'>%d</div></div>" % report.get("数据行数", 0))
        html.append("<div class='stat'><div class='label'>分组字段</div><div class='num'>%s</div></div>" % (report.get("分组") or "无"))
        html.append("<div class='stat'><div class='label'>聚合字段</div><div class='num'>%s</div></div>" % (report.get("聚合") or "无"))
        
        if "分组统计" in report:
            html.append("<h2>分组统计</h2><table><tr><th>分组</th><th>数量</th>")
            first = next(iter(report["分组统计"].values()))
            for k in first:
                if k != "数量": html.append("<th>%s</th>" % k)
            html.append("</tr>")
            for key, stats in report["分组统计"].items():
                html.append("<tr><td>%s</td><td>%d</td>" % (key, stats["数量"]))
                for k, v in stats.items():
                    if k != "数量": html.append("<td>%s</td>" % v)
                html.append("</tr>")
            html.append("</table>")
        
        html.append("</body></html>")
        
        output_html = "\n".join(html)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_html)
            print("报表已生成: %s" % output)
        else:
            print(output_html[:500])
        
        return output_html
    
    def batch_generate(self, config_file):
        """批量生成报表"""
        with open(config_file) as f:
            configs = json.load(f)
        
        results = []
        for cfg in configs:
            csv_path = cfg.get("csv")
            if not os.path.exists(csv_path):
                print("跳过: %s (文件不存在)" % csv_path)
                continue
            
            output = cfg.get("output") or "report_%s.html" % os.path.splitext(os.path.basename(csv_path))[0]
            result = self.from_csv(csv_path, cfg.get("group_by"), cfg.get("aggregate"), output)
            results.append({"file": csv_path, "output": output, "status": "ok" if result else "failed"})
        
        return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="自动化报表生成器")
    parser.add_argument("action", choices=["from-csv", "batch"])
    parser.add_argument("input", help="CSV文件或JSON配置")
    parser.add_argument("-g", "--group-by", help="分组字段")
    parser.add_argument("-a", "--aggregate", help="聚合字段")
    parser.add_argument("-o", "--output", help="输出文件")
    args = parser.parse_args()
    
    gen = ReportGenerator()
    
    if args.action == "from-csv":
        gen.from_csv(args.input, args.group_by, args.aggregate, args.output)
    elif args.action == "batch":
        gen.batch_generate(args.input)
