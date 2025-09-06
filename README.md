# falcon-containment-automation

A small, hands-on project that shows how to **contain** a Windows 11 VM with CrowdStrike Falcon (block its network), **lift** containment (restore network), and export a **Top-10 vulnerabilities** CSV from Spotlight. It uses simple Python scripts on Ubuntu to call the Falcon API and saves clear proof (screenshots + CSV) for your portfolio.

---

## What this project does
- **Contain a host:** Put a Windows 11 VM into network containment from the Falcon API.
- **Lift containment:** Restore normal network access.
- **Prove the result:** Run a TCP test (port 443) in the VM to show blocked vs. allowed.
- **Export fixes:** Pull a “Top-10 Spotlight” CSV to prioritize patches.

---

## What’s in the repo

```

scripts/
autocontain\_v2.py      # contain / lift (recommended)
device\_check.py        # show host details (platform, version, state)
spotlight\_top10.py     # export Top-10 vulnerabilities to CSV
autocontain.py         # baseline version used in the lab

reports/                 # put top10\_spotlight.csv here
screenshots/             # proof images:
\#   falconcontained.png
\#   falconnormal.png
\#   vmcontained.png
\#   vmlifted.png
README.md
requirements.txt

````

> **Do not commit secrets.** Keep API keys in a local `.env` file that is not pushed to GitHub.

---

## Prerequisites
- CrowdStrike Falcon tenant with **API client** (Client ID/Secret).
- A Windows 11 VM with the Falcon sensor installed (e.g., host name `MANDAVA`).
- An Ubuntu machine (can be a VM) with Python 3.10+ and internet access.

---

## Setup (Ubuntu)
1) Create a Python environment and install packages:
```bash
python3 -m venv ~/.venv_capstone
~/.venv_capstone/bin/pip install -r requirements.txt
````

2. Create `~/.env` (local only, not in git):

```bash
cat > ~/.env << 'EOF'
CS_BASE=https://api.us-2.crowdstrike.com
CS_CLIENT_ID=YOUR_CLIENT_ID
CS_CLIENT_SECRET=YOUR_CLIENT_SECRET
EOF
```

---

## Run the demo

> Replace `MANDAVA` if your Windows VM host name is different.

**Contain the VM**

```bash
~/.venv_capstone/bin/python scripts/autocontain_v2.py --host MANDAVA
```

**Lift containment**

```bash
~/.venv_capstone/bin/python scripts/autocontain_v2.py --host MANDAVA --lift
```

---

## Verify the result (quick proof)

Inside the **Windows 11 VM** (PowerShell):

* **While contained** (should fail)

```powershell
Test-NetConnection 1.1.1.1 -Port 443
```

* **After lift** (should succeed)

```powershell
Test-NetConnection 1.1.1.1 -Port 443
```

Also capture the Falcon device page showing **Contained** → **Normal**.

---

## Export Top-10 Spotlight CSV

```bash
~/.venv_capstone/bin/python scripts/spotlight_top10.py --host MANDAVA
# Output: reports/top10_spotlight.csv
```

---

## Evidence

* Falcon device page — contained → normal
  ![Contained](screenshots/falconcontained.png)
  ![Normal](screenshots/falconnormal.png)

* VM network while contained (TCP/443 blocked)
  ![443 blocked](screenshots/vmcontained.png)

* After lift (TCP/443 allowed)
  ![443 open](screenshots/vmlifted.png)

* Top-10 Spotlight fixes
  `reports/top10_spotlight.csv`

---

## Troubleshooting (brief)

* **Contain says “not eligible”:**
  Start required services in the VM, then try again:

  ```powershell
  sc start BFE; sc start MpsSvc; Restart-Service CSFalconService -Force
  ```
* **CSV is empty:** Spotlight can take time to populate after the sensor comes online.

---

## Safety

* Don’t commit `.env` or any API keys.
* Use this only with **test VMs**, not production systems.

---

```
::contentReference[oaicite:0]{index=0}
```
