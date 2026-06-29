import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jobspy import scrape_jobs

# 1. LIVE SEARCH PARAMETERS
SEARCH_TERM = "Infrastructure Architect Director SRE TPM"
LOCATION = "Bengaluru, India"

SENDER_EMAIL = "abhinav.abhinavkhare@gmail.com"
SENDER_PASSWORD = "iyrtpyadbahciwcq"  # Your secure 16-character code
RECEIVER_EMAIL = "abhinav_khare2002@yahoo.com"

DB_FILE = "sent_jobs.txt"

def load_sent_jobs():
    """Loads previously emailed job URLs so we don't repeat them."""
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_jobs(new_urls):
    """Appends newly emailed job URLs to our tracker file."""
    with open(DB_FILE, "a", encoding="utf-8") as f:
        for url in new_urls:
            f.write(f"{url}\n")

def fetch_premium_jobs():
    print(f"Scraping live listings from LinkedIn & Indeed for {LOCATION}...")
    try:
        jobs_df = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=SEARCH_TERM,
            location=LOCATION,
            results_per_site=25,
            hours_old=72,        # Captures active roles over the last 3 days
            country_indeed='india'
        )
        
        sent_urls = load_sent_jobs()
        matched_jobs = []
        new_urls_to_save = []
        
        if not jobs_df.empty:
            for _, row in jobs_df.iterrows():
                job_url = row.get('job_url', '')
                
                # SKIP if we have already sent this job URL in a previous run
                if not job_url or job_url in sent_urls:
                    continue
                    
                title = row.get('title', 'Technical Role')
                company = row.get('company', 'Enterprise Client')
                job_location = row.get('location', LOCATION)
                
                matched_jobs.append({
                    'title': title,
                    'company': company,
                    'url': job_url,
                    'location': job_location
                })
                new_urls_to_save.append(job_url)
                
        return matched_jobs, new_urls_to_save
    except Exception as e:
        print(f"Scraping engine encounter: {e}")
        return [], []

def send_email_digest(jobs_list, new_urls_to_save):
    if not jobs_list:
        print("No brand-new localized matches found since the last run.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"New Premium Job Digest: {len(jobs_list)} Fresh Roles Found"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Executive Job Hunt Digest: Bengaluru Ecosystem</h2>
        <p>The following <strong>new</strong> roles matching your profile were found:</p>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%; border-color: #ddd;">
          <tr style="background-color: #f2f2f2;">
            <th align="left">Designation</th>
            <th align="left">Company</th>
            <th align="left">Location</th>
            <th align="center">Action</th>
          </tr>
    """
    
    for job in jobs_list:
        html += f"""
          <tr>
            <td><strong>{job['title']}</strong></td>
            <td>{job['company']}</td>
            <td>{job['location']}</td>
            <td align="center"><a href="{job['url']}" style="background-color: #007bff; color: white; padding: 6px 12px; text-decoration: none; border-radius: 3px; display: inline-block; font-size: 13px;">Apply Now</a></td>
          </tr>
        """
        
    html += """
        </table>
        <br>
        <p style="font-size: 11px; color: #777;">This is an automated utility tracking high-bracket regional tech positions.</p>
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
        print("Daily digest successfully emailed!")
        
        # Only remember them if the email actually sent out successfully
        save_sent_jobs(new_urls_to_save)
        
    except Exception as e:
        print(f"Failed to transmit email: {e}")

if __name__ == "__main__":
    unique_jobs, urls_to_track = fetch_premium_jobs()
    print(f"Found {len(unique_jobs)} fresh, unsent opportunities.")
    send_email_digest(unique_jobs, urls_to_track)