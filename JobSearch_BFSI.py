import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jobspy import scrape_jobs

# 1. CORE BFSI TARGET PARAMETERS
#SEARCH_TERM = '(Infrastructure OR SRE OR "Enterprise Architecture" OR DevOps) AND (Director OR VP OR Lead OR Manager)'
SEARCH_TERM = '(Infrastructure OR SRE OR "Enterprise Architecture" OR DevOps) AND (Director OR VP OR Lead) ' \
'              AND ("JPMorgan" OR "Wells Fargo" OR "Goldman Sachs" OR "Morgan Stanley" OR "Citi" OR "Barclays" ' \
               'OR "HSBC" OR "Deutsche" OR "Fidelity")'
LOCATION = "India"

# Exact and partial string match matrix for major Global Capability Centers (GCCs) & Banks
BFSI_COMPANIES = [
    "goldman sachs", "goldman", "wells fargo", "jpmorgan", "jp morgan", "chase", 
    "morgan stanley", "bank of america", "bofa", "citi", "citibank", "hsbc", "barclays", 
    "standard chartered", "fidelity", "ubs", "deutsche bank", "deutsche", "bny mellon", "bny",
    "icici", "hdfc", "axis bank", "kotak", "sbi", "fis global", "fis", "fiserv", "macquarie",
    "societe generale", "natwest", "lloyds", "standard chartered bank", "am权", "bnp paribas",
    "nomura", "northern trust", "invesco", "blackrock", "allianz", "prudential"
]

SENDER_EMAIL = "abhinav.abhinavkhare@gmail.com"
SENDER_PASSWORD = "********"  # Your secure 16-character code
RECEIVER_EMAIL = "abhinav_khare2002@yahoo.com"

DB_FILE = "sent_bfsi_jobs.txt"  # Isolated history tracking file for version 2.0

def load_sent_jobs():
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_jobs(new_urls):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        for url in new_urls:
            f.write(f"{url}\n")

def fetch_bfsi_jobs():
    print(f"Scraping LinkedIn & Indeed specifically for BFSI Institutional roles in {LOCATION}...")
    try:
        # Increase results per site to broaden initial pool before company filtering
        jobs_df = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=SEARCH_TERM,
            location=LOCATION,
            results_per_site=250,
            hours_old=72,
            country_indeed='india'
        )
        
        sent_urls = load_sent_jobs()
        matched_jobs = []
        new_urls_to_save = []
        
        if not jobs_df.empty:
            for _, row in jobs_df.iterrows():
                job_url = row.get('job_url', '')
                if not job_url or job_url in sent_urls:
                    continue
                
                company_name = str(row.get('company', '')).strip()
                company_lower = company_name.lower()
                
                # CRITICAL: Verify if the posting belongs to our curated BFSI target list
                if any(bfsi in company_lower for bfsi in BFSI_COMPANIES):
                    title = row.get('title', 'Technical Leadership Role')
                    job_location = row.get('location', LOCATION)
                    
                    matched_jobs.append({
                        'title': title,
                        'company': company_name,
                        'url': job_url,
                        'location': job_location
                    })
                    new_urls_to_save.append(job_url)
                    
        return matched_jobs, new_urls_to_save
    except Exception as e:
        print(f"BFSI Scraper pipeline error: {e}")
        return [], []

def send_bfsi_email_digest(jobs_list, new_urls_to_save):
    if not jobs_list:
        print("No new premier BFSI institutional matches identified since last run.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🔒 BFSI Premium Job Alert: {len(jobs_list)} New Roles Found"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #1a365d;">Abhinav's BFSI Capital Markets Job Hunt Digest (India)</h2>
        <p>The following new high-bracket roles were discovered within top tier FinTech and Banking GCCs:</p>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%; border-color: #cbd5e1;">
          <tr style="background-color: #1a365d; color: white;">
            <th align="left">Designation</th>
            <th align="left">Financial Institution</th>
            <th align="left">Location</th>
            <th align="center">Action</th>
          </tr>
    """
    
    for job in jobs_list:
        html += f"""
          <tr>
            <td><strong>{job['title']}</strong></td>
            <td style="color: #1e3a8a; font-weight: bold;">{job['company']}</td>
            <td>{job['location']}</td>
            <td align="center"><a href="{job['url']}" style="background-color: #1a365d; color: white; padding: 6px 12px; text-decoration: none; border-radius: 3px; display: inline-block; font-size: 13px; font-weight: bold;">Review Position</a></td>
          </tr>
        """
        
    html += """
        </table>
        <br>
        <p style="font-size: 11px; color: #64748b;">This is a premium version 2.0 script tracking global banking infrastructure operations.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    try:
        print("Connecting to secure mail server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("BFSI premium digest successfully emailed!")
        save_sent_jobs(new_urls_to_save)
    except Exception as e:
        print(f"Failed to transmit email payload: {e}")

if __name__ == "__main__":
    unique_jobs, urls_to_track = fetch_bfsi_jobs()
    print(f"Isolated {len(unique_jobs)} premium banking sector listings.")
    send_bfsi_email_digest(unique_jobs, urls_to_track)
