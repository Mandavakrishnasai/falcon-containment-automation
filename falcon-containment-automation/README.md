
# falcon-containment-automation

Hands-on project that shows how to **contain** a Windows 11 VM with CrowdStrike Falcon (block its network), **lift** containment (restore network), and export a **Top-10 vulnerabilities** CSV from Spotlight. Simple Python scripts on Ubuntu call the Falcon API. Screenshots + CSV provide clear proof for your portfolio.

## Included
- `scripts/autocontain_v2.py` — contain/lift with proper 200/202 handling
- `scripts/device_check.py` — host details (platform, agent, containment state, policy IDs)
- `scripts/autocontain.py`, `scripts/spotlight_top10.py` — baseline lab scripts
- `reports/` — generated artifacts (e.g., `top10_spotlight.csv`)
- `screenshots/` — proof images
- `.gitignore` — keeps secrets and local files out

> **Do NOT commit secrets.** Keep `.env` local-only.

## How to run
```bash
python3 -m venv ~/.venv_capstone
~/.venv_capstone/bin/pip install -r requirements.txt

# ~/.env (not committed)
# CS_BASE=https://api.us-2.crowdstrike.com
# CS_CLIENT_ID=...
# CS_CLIENT_SECRET=...
````

Contain / lift:

```bash
~/.venv_capstone/bin/python scripts/autocontain_v2.py --host MANDAVA
~/.venv_capstone/bin/python scripts/autocontain_v2.py --host MANDAVA --lift
```

Spotlight Top-10:

```bash
~/.venv_capstone/bin/python scripts/spotlight_top10.py --host MANDAVA
# output: reports/top10_spotlight.csv
```

(Optional) Host snapshot:

```bash
~/.venv_capstone/bin/python scripts/device_check.py --host MANDAVA
```

## Evidence

* Falcon UI: contained → normal (screenshots)
* VM TCP test: 1.1.1.1:443 blocked while contained, allowed after lift
* `reports/top10_spotlight.csv`

## Troubleshooting

* **“Not eligible” on contain:** in the VM, start required services and retry:

  ```powershell
  sc start BFE; sc start MpsSvc; Restart-Service CSFalconService -Force
  ```
* **CSV empty:** Spotlight may need time after the sensor first checks in.

## Skills

EDR/API (FalconPy) • Incident Response (contain/lift) • Exposure Management (Spotlight) • Reproducible docs

````
