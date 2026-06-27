#!/usr/bin/env python3
"""Excel数据分析仪表盘 - 自动生成统计图表和报告"""
import os, sys, json
from collections import Counter, defaultdict
import csv, datetime

def analyze_csv(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        return {"error": "空文件"}
    
    columns = list(rows[0].keys())
    report = {
        "文件名": os.path.basename(filepath),
        "行数": len(rows),
        "列数": len(columns),
        "列名": columns,
        "分析时间": datetime.datetime.now().isoformat(),
        "列分析": {}
    }
    
    for col in columns:
        values = [r[col] for r in rows if r[col]]
        numeric_vals = []
        for v in values:
            try: numeric_vals.append(float(v))
            except: pass
        
        col_analysis = {
            "非空值": len(values),
            "空值": len(rows) - len(values),
            "唯一值": len(set(values)),
        }
        
        if numeric_vals:
            col_analysis.update({
                "类型": "数值",
                "最小值": min(numeric_vals),
                "最大值": max(numeric_vals),
                "平均值": round(sum(numeric_vals)/len(numeric_vals), 2),
                "中位数": sorted(numeric_vals)[len(numeric_vals)//2],
                "总和": round(sum(numeric_vals), 2)
            })
        
        if len(set(values)) <= 20 and len(values) > 0:
            counter = Counter(values)
            col_analysis["类型"] = "分类"
            col_analysis["分布"] = dict(counter.most_common(10))
        
        report["列分析"][col] = col_analysis
    
    return report

def generate_html_report(report, output_path):
    html = ['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">']
    html.append(f'<title>数据分析报告 - {report["文件名"]}</title>')
    html.append('<style>body{font-family:sans-serif;background:#1a1a2e;color:#e0e0e0;padding:20px}')
    html.append('h1{color:#FFD700}.card{background:#16213e;border-radius:8px;padding:15px;margin:10px 0}')
    html.append('.num{font-size:1.5em;color:#FFD700;font-weight:bold}')
    html.append('.stat{display:inline-block;margin:10px;padding:15px;background:#0f3460;border-radius:8px;min-width:120px}')
    html.append('table{width:100%;border-collapse:collapse;margin:10px 0}')
    html.append('th,td{padding:8px;text-align:left;border-bottom:1px solid #2a2a4e}')
    html.append('th{color:#FFD700}')
    html.append('</style></head><body>')
    
    html.append(f'<h1>📊 数据分析报告</h1>')
    html.append(f'<p>文件: {report["文件名"]} | 行数: {report["行数"]} | 列数: {report["列数"]}</p>')
    html.append(f'<p>分析时间: {report["分析时间"]}</p>')
    
    html.append('<div class="card"><h2>📋 列分析</h2>')
    for col, analysis in report["列分析"].items():
        html.append(f'<h3>{col}</h3><table><tr>')
        for k, v in list(analysis.items())[:6]:
            val = str(v)[:50] if isinstance(v, (list, dict)) else str(v)
            html.append(f'<th>{k}</th><td>{val}</td>')
        html.append('</tr></table>')
    html.append('</div>')
    
    if any(a.get("类型") == "数值" for a in report["列分析"].values()):
        html.append('<div class="card"><h2>📈 数值统计</h2>')
        for col, a in report["列分析"].items():
            if a.get("类型") == "数值":
                html.append(f'<div class="stat"><div>{col}</div>')
                html.append(f'<div class="num">{a["平均值"]}</div>')
                html.append(f'<div>min:{a["最小值"]} max:{a["最大值"]}</div></div>')
        html.append('</div>')
    
    html.append('</body></html>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))
    
    return output_path

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='数据分析仪表盘')
    parser.add_argument('input', help='CSV文件路径')
    parser.add_argument('-o', '--output', help='输出HTML报告路径')
    args = parser.parse_args()
    
    report = analyze_csv(args.input)
    if "error" in report:
        print(f"错误: {report['error']}")
        sys.exit(1)
    
    output = args.output or f"report_{os.path.splitext(os.path.basename(args.input))[0]}.html"
    generate_html_report(report, output)
    print(f"报告已生成: {output}")
    print(f"共 {report['行数']} 行, {report['列数']} 列")
