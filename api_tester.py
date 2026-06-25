#!/usr/bin/env python3
"""API Tester - Automated endpoint testing with reporting.
Price: $15"""
import requests, json, sys, time
def test(endpoints_file, output="report.json"):
    with open(endpoints_file) as f:
        endpoints = json.load(f)
    results = []
    for ep in endpoints:
        t0 = time.time()
        try:
            r = requests.request(ep.get("method","GET"), ep["url"], timeout=10)
            results.append({"url":ep["url"],"status":r.status_code,"time":time.time()-t0,"pass":r.status_code < 500})
        except Exception as e:
            results.append({"url":ep["url"],"error":str(e),"pass":False})
    json.dump(results, open(output,"w"), indent=2)
    passed = sum(1 for r in results if r.get("pass"))
    print("%d/%d passed" % (passed, len(results)))
if __name__ == "__main__":
    test(sys.argv[1]) if len(sys.argv)>1 else print("Usage: python api_tester.py <endpoints.json>")
