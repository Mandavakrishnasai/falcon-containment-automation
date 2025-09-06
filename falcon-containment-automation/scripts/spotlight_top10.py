#!/usr/bin/env python3
import os, sys, csv
from pathlib import Path
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None
from falconpy import Hosts, SpotlightVulnerabilities

def env():
    if load_dotenv:
        for p in [Path('~/.env').expanduser(), Path('.env').resolve()]:
            if p.exists(): load_dotenv(dotenv_path=p); break
    for k in ("CS_CLIENT_ID","CS_CLIENT_SECRET"):
        if not os.getenv(k): sys.exit(f"Missing {k}")

def client(api):
    base = os.getenv("CS_BASE", "https://api.us-2.crowdstrike.com")
    return api(client_id=os.getenv("CS_CLIENT_ID"), client_secret=os.getenv("CS_CLIENT_SECRET"), base_url=base)

if __name__ == "__main__":
    env()
    hosts = client(Hosts); spt = client(SpotlightVulnerabilities)
    if "--host" not in sys.argv: sys.exit("Usage: spotlight_top10.py --host <HOSTNAME>")
    host = sys.argv[sys.argv.index("--host")+1]
    q = hosts.query_devices_by_filter(filter=f'hostname:\"{host}\"', limit=1); aid = q["body"]["resources"][0]
    res = spt.query_vulnerabilities_combined(filter=f\"aid:'{aid}'\", limit=10, sort=\"severity|desc\")
    Path("reports").mkdir(exist_ok=True); out = Path("reports/top10_spotlight.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cve","severity","status","featured_exploit","product_name","remediation"])
        for v in res.get("body",{}).get("resources",[]):
            w.writerow([
                v.get("cve_id"), v.get("severity"), v.get("status"), v.get("featured_exploit"),
                (v.get("product","") or v.get("product_name","")), (v.get("remediation","") or v.get("solution",""))
            ])
    print(f"[+] Wrote {out}")
