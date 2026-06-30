# Jobseekers
It includes the script for finding the job in LinkedIn and Indeed job portal nd send an email to my pesonal id. It also filter out the previous search results which has been already shared.It also another version which can search for only BFSI domains.
----------------------
```python
import os

readme_content = """# Automated Executive Job Search Utilities

This repository contains two production-ready, automated scraping utilities tailored for tracking high-bracket infrastructure and technical leadership positions across the Indian tech ecosystem and Global Capability Centers (GCCs). The scripts bypass complex browser-based scraping barriers and leverage the `jobspy` library to deliver real-time, deduplicated job matches straight to your email inbox.

---

## 🛠️ System Architecture & Workflow

Both versions operate on a data-pipeline model designed to avoid duplicate notifications and maximize data density within your daily execution windows:

1. **Scraping Engine:** Connects via `jobspy` to extract live, structured job metadata from global professional networks.
2. **Local Stateful Deduplication:** Matches newly extracted URLs against an isolated tracking text file (`sent_jobs.txt` or `sent_bfsi_jobs.txt`). Already-notified roles are stripped instantly.
3. **MIME HTML Compilation:** Packages remaining unique openings into a responsive HTML table featuring quick-action application buttons.
4. **Secure SMTP Relay:** Authenticates via Google's secure App Passwords layer to transmit the final digest cleanly to your destination address.

---

## 📂 Version Directory & Specifications

### 1. General Leadership Utility (`JobSearch.py`)
* **Objective:** Tracks the broader premium technology market for elite localized roles.
* **Scope:** Focused primarily on the regional hub (**Bengaluru, India**).
* **Target Profile:** Explores open-market roles across enterprise software, engineering clients, and tier-1 tech firms.
* **Search Phrase Logic:**
  `"Infrastructure Architect Director SRE TPM"`

### 2. Institutional BFSI Capital Markets Utility (`JobSearch_BFSI.py`)
* **Objective:** Isolates high-bracket infrastructure operations strictly within major global financial institutions and banking GCCs.
* **Scope:** Broadened across **India** to capture remote operations and distributed banking hubs (Bengaluru, Mumbai, Pune, Hyderabad).
* **Target Profile:** Targets Vice President (VP), Director, and Senior Lead positions within elite financial environments.
* **Advanced Boolean Query Parsing:**
  `(Infrastructure OR SRE OR "Enterprise Architecture" OR DevOps) AND (Director OR VP OR Lead) AND ("JPMorgan" OR "Wells Fargo" OR "Goldman Sachs" OR "Morgan Stanley" OR "Citi" OR "Barclays" OR "HSBC" OR "Deutsche" OR "Fidelity")`

---

## ⚙️ Prerequisites & Environment Setup

Ensure your local terminal session is locked into a stable, pre-compiled runtime environment to avoid native C-compiler source build exceptions.

### 1. Library Dependencies
Install the latest stable build of `python-jobspy` utilizing the Windows Python Launcher to guarantee correct path binding:

```

```text
README.md generated successfully.

```bash
py -3.12 -m pip install python-jobspy --upgrade

```

### 2. Secure Mail Configuration

Before executing either script, update the following configuration variables located at the top of the files:

* `SENDER_EMAIL`: Your dedicated dispatch Gmail address.
* `SENDER_PASSWORD`: Your unique, **16-character Google App Password** (generated under *Google Account Security -> 2-Step Verification -> App Passwords*).
* `RECEIVER_EMAIL`: Your primary destination inbox (e.g., Yahoo Mail).

---

## 🚀 Execution Guide

Run the scripts directly via the terminal using the explicitly targeted Python 3.12 environment runner to bypass default path conflicts:

### Run General Regional Search:

```bash
py -3.12 JobSearch.py

```

### Run Institutional BFSI Scraper:

```bash
py -3.12 JobSearch_BFSI.py

```

---

## 💾 State Preservation & Maintenance

* **Deduplication Files:** On the first execution, the utilities will automatically generate local tracking files (`sent_jobs.txt` and `sent_bfsi_jobs.txt`).
* **Resetting the Pipeline:** If you ever wish to re-receive previously filtered listings or test formatting adjustments, simply delete the respective `.txt` file from your project folder, and the script will flush the cache and run a comprehensive pull.
"""

```

This file is structured in a clean, professional technical document layout that maps out the underlying architecture, Boolean search logics, system prerequisites, and unambiguous execution paths.

### What is included inside the README:
1. **Architecture Overview:** An operational map explaining how the data flows from `jobspy` into your stateful local filters and exits through your secure SMTP relay.
2. **Detailed Version Specifications:** Clear delineations between how **Version 1.0 (General - Bengaluru focused)** and **Version 2.0 (BFSI - India-wide Boolean grouped)** parse searches.
3. **Environmental Prerequisites:** Hardcoded, foolproof path commands using the `py -3.12` launcher shortcut to ensure dependencies remain aligned with your correct Python runtime.
4. **Maintenance Tips:** Detailed instructions explaining how the automatic `.txt` file caching works and how to force-reset the historical data logs if you ever want a full clean refresh.

You can drop this directly into your `JobSearch-Utility` workspace folder so your repository remains organized and document-complete! Let me know how the updated direct-bank query runs on your next execution sweep.

```
