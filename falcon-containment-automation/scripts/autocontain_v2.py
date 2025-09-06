#!/usr/bin/env python3
import os, sys, argparse
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
                load_dotenv(dotenv_path=candidate)
                break

def require_env(key: str) -> str:
    v = os.getenv(key)
    if not v:
        print(f"[!] Missing env: {key}", file=sys.stderr); sys.exit(2)
    return v

def get_client():
    base = os.getenv("CS_BASE", "https://api.us-2.crowdstrike.com")
    cid  = require_env("CS_CLIENT_ID")
    sec  = require_env("CS_CLIENT_SECRET")
    return Hosts(client_id=cid, client_secret=sec, base_url=base)

def get_aid_by_hostname(client: Hosts, name: str) -> str:
    r = client.query_devices_by_filter(filter=f'hostname:\"{name}\"', limit=1)
    if r.get("status_code") != 200 or not r.get("body", {}).get("resources"):
        print(f"[!] Host '{name}' not found. Response: {r}", file=sys.stderr); sys.exit(3)
    return r["body"]["resources"][0]

def perform(client: Hosts, action: str, aid: str):
    r = client.perform_action(action_name=action, body={"ids": [aid]})
    code = r.get("status_code", 0)
    body = r.get("body", {})
    if code in (200, 202):
        print(f"[+] Action '{action}' accepted for AID {aid} (status {code})."); return
    if code == 409:
        print(f"[!] '{action}' 409 Not eligible — host may already be in that state, or endpoint prereqs not met.", file=sys.stderr)
    else:
        print(f"[!] '{action}' failed. Status: {code}. Body: {body}", file=sys.stderr)
    sys.exit(4)

if __name__ == "__main__":
    try_load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--host"); ap.add_argument("--aid")
    ap.add_argument("--lift", action="store_true")
    a = ap.parse_args()
    h = get_client()
    aid = a.aid or (get_aid_by_hostname(h, a.host) if a.host else None)
    if not aid: sys.exit("[!] Provide --host or --aid")
    act = "lift_containment" if a.lift else "contain"
    perform(h, act, aid)
