#!/usr/bin/env python3
import os, sys, argparse, json
from pathlib import Path
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None
from falconpy import Hosts

def try_load_env():
    if load_dotenv:
        for candidate in [Path('~/.env').expanduser(), Path('.env').resolve()]:
            if candidate.exists():
                load_dotenv(dotenv_path=candidate); break

def require_env(key: str) -> str:
    v = os.getenv(key)
    if not v: print(f"[!] Missing env: {key}", file=sys.stderr); sys.exit(2)
    return v

def get_client():
    base = os.getenv("CS_BASE", "https://api.us-2.crowdstrike.com")
    cid  = require_env("CS_CLIENT_ID")
    sec  = require_env("CS_CLIENT_SECRET")
    return Hosts(client_id=cid, client_secret=sec, base_url=base)

if __name__ == "__main__":
    try_load_env()
    p = argparse.ArgumentParser(); p.add_argument("--host", required=True)
    a = p.parse_args()
    h = get_client()
    q = h.query_devices_by_filter(filter=f'hostname:\"{a.host}\"', limit=1)
    if q.get("status_code") != 200 or not q.get("body", {}).get("resources"):
        print(f"[!] Host '{a.host}' not found. Response: {q}", file=sys.stderr); sys.exit(3)
    aid = q["body"]["resources"][0]
    d = h.get_device_details(ids=[aid])
    res = d.get("body", {}).get("resources", [])
    if not res: print(f"[!] No details for AID {aid}. Raw: {d}", file=sys.stderr); sys.exit(4)
    info = res[0]
    out = {
        "aid": aid,
        "hostname": info.get("hostname"),
        "platform_name": info.get("platform_name"),
        "os_version": info.get("os_version"),
        "agent_version": info.get("agent_version"),
        "last_seen": info.get("last_seen"),
        "containment_state": info.get("containment_state"),
        "device_policies": info.get("device_policies", {}),
        "tags": info.get("tags", []),
        "cid": info.get("cid")
    }
    print(json.dumps(out, indent=2))
