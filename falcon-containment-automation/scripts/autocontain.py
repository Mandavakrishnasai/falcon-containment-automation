#!/usr/bin/env python3
import os, sys, argparse
from pathlib import Path
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None
from falconpy import Hosts

def load_env():
    if load_dotenv:
        for p in [Path('~/.env').expanduser(), Path('.env').resolve()]:
            if p.exists():
                load_dotenv(dotenv_path=p); break
    for k in ("CS_CLIENT_ID","CS_CLIENT_SECRET"):
        if not os.getenv(k): sys.exit(f"Missing {k}")

def client():
    base = os.getenv("CS_BASE", "https://api.us-2.crowdstrike.com")
    return Hosts(client_id=os.getenv("CS_CLIENT_ID"), client_secret=os.getenv("CS_CLIENT_SECRET"), base_url=base)

if __name__ == "__main__":
    load_env(); ap = argparse.ArgumentParser()
    ap.add_argument("--host"); ap.add_argument("--lift", action="store_true")
    a = ap.parse_args(); h = client()
    if not a.host: sys.exit("Provide --host")
    q = h.query_devices_by_filter(filter=f'hostname:\"{a.host}\"', limit=1)
    aid = q["body"]["resources"][0]
    act = "lift_containment" if a.lift else "contain"
    r = h.perform_action(action_name=act, body={"ids":[aid]})
    print(r)
