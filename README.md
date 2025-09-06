# falcon-containment-automation

A small, hands-on project that shows how to **contain** a Windows 11 VM with CrowdStrike Falcon (block its network), **lift** containment (restore network), and export a **Top-10 vulnerabilities** CSV from Spotlight. It uses a simple Python script on Ubuntu to call the Falcon API and saves clear proof (screenshots + CSV) for your portfolio.

---

## What this project does

* **Contain a host:** Put a Windows 11 VM into network containment from the Falcon API.
* **Lift containment:** Restore normal network access.
* **Prove the result:** Run a quick TCP test (port 443) in the VM to show blocked vs. allowed.
* **Export fixes:** Pull a “Top-10 Spotlight” CSV so you can prioritize patches.

---

## What’s in the repo

```
scripts/
  autocontain_v2.py      # contain / lift
  device_check.py        # show host details (platform, version, state)
  spotlight_top10.py     # export Top-10 vulnerabilities to CSV

reports/                 # generated CSV goes here (add your file)
screenshots/             # add your screenshots here
README.md
requirements.txt
.gitignore               # keeps secrets and local files out of git
```

---

## Prerequisites

* CrowdStrike Falcon tenant with **API client** (Client ID/Secret).
* A Windows 11 VM with the Falcon sensor installed (e.g., host name `MANDAVA`).
* An Ubuntu machine (can be a VM) with Python 3.10+ and internet access.

> **Do not commit secrets.** Keep your API keys in a local `.env` file.

---

## Setup (Ubuntu)

1. Create a Python environment and install packages:

```bash
python3 -m venv ~/.venv_capstone
~/.venv_capstone/bin/pip install -r requirements.txt
```

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

> Replace `MANDAVA` with your Windows VM host name if different.

**Contain the VM:**

```bash
~/.venv_capstone/bin/python scripts/autocontain_v2.py --host MANDAVA
```

**Lift containment:**

```bash
~/.venv_capstone/bin/python scripts/autocontain_v2.py --host MANDAVA --lift
```

---

## Verify the result (quick, visual proof)

Inside the **Windows 11 VM** (PowerShell):

* **While contained** (should fail):

```powershell
Test-NetConnection 1.1.1.1 -Port 443
```

* **After lift** (should succeed):

```powershell
Test-NetConnection 1.1.1.1 -Port 443
```

Also capture the Falcon device page showing status changing between **Contained** and **Normal**.

> Save your images in `screenshots/` (e.g., `falcon-contained.png`, `falcon-normal.png`, `vm-contained-443.png`, `vm-lifted-443.png`).

---

## Export Top-10 Spotlight CSV

```bash
~/.venv_capstone/bin/python scripts/spotlight_top10.py --host MANDAVA
# Output: reports/top10_spotlight.csv
```

Add the CSV to your repo to show prioritised fixes.

---

## What to show in your portfolio

* Falcon device page: **Contained** → **Normal**
* VM results: 443 **blocked** while contained, **allowed** after lift
* `reports/top10_spotlight.csv`

This gives a simple, credible story: “I can contain a host, prove the impact, and pull a fix list.”

---

## Troubleshooting (brief)

* **Contain says “not eligible”:**

  * Make sure Windows Firewall and Base Filtering Engine services are running in the VM:

    ```powershell
    sc start BFE; sc start MpsSvc
    ```
  * Restart the Falcon service:

    ```powershell
    Restart-Service CSFalconService -Force
    ```
  * Try contain again.

* **CSV is empty:** Spotlight may need time to populate after the sensor comes online.

---

## Safety and privacy

* Do not commit `.env` or any keys.
* This lab is designed for **test VMs** only, not production systems.

---

## License

Use freely for learning and job portfolios. If you share or adapt, please credit the original repo name.
