import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jobspy import scrape_jobs  # Bypasses blocks across major portals

KEYWORDS = ["Director Infrastructure", "Principal Architect", "Senior TPM"]
LOCATION = "Bengaluru, India"
SENDER_EMAIL = "abhinav.abhinavkhare@gmail.com"
SENDER_PASSWORD = "iyrtpyadbahciwcq" 
RECEIVER_EMAIL = "abhinav_khare2002@yahoo.com"

def aggregate_market_jobs():
    print(f"Querying LinkedIn & Indeed for premium roles in {LOCATION}...")
    try:
        # Scrapes across major active networks safely without individual platform APIs
        jobs_df = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=" ".join(KEYWORDS),
            location=LOCATION,
            results_per_site=15,
            hours_old=72 # Tracks fresh openings over the last 3 days
        )
        
        # Format pandas dataframe results into a standard list of dictionaries
        jobs_list = []
        for _, row in jobs_df.iterrows():
            jobs_list.append({
                'title': row.get('title'),
                'company': row.get('company'),
                'url': row.get('job_url'),
                'location': row.get('location')
            })
        return jobs_list
    except Exception as e:
        print(f"Scraping interface error: {e}")
        return []

def send_email_digest(jobs_list):
    """
    Formats the matching results into an email digest and sends it.
    """
    if not jobs_list:
        print("No new matches found today to email.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Daily Executive Job Digest: {len(jobs_list)} New Roles Found"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    # Construct clean HTML layout
    html = """
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Abhinav's Executive Job Hunt Digest</h2>
        <p>The following high-level roles matching your profile were discovered:</p>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
          <tr style="background-color: #f2f2f2;">
            <th>Designation</th>
            <th>Company</th>
            <th>Location</th>
            <th>Action</th>
          </tr>
    """
    
    for job in jobs_list:
        html += f"""
          <tr>
            <td><strong>{job['title']}</strong></td>
            <td>{job['company']}</td>
            <td>{job['location']}</td>
            <td><a href="{job['url']}" style="background-color: #007bff; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">Apply Now</a></td>
          </tr>
        """
        
    html += """
        </table>
        <br>
        <p style="font-size: 12px; color: #777;">This is an automated utility tracking high-bracket positions.</p>
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
    except Exception as e:
        print(f"Failed to transmit email: {e}")

if __name__ == "__main__":
    aggregated_jobs = []
    for kw in KEYWORDS:
        found_jobs = fetch_jobs(kw, LOCATION)
        aggregated_jobs.extend(found_jobs)
        
    # Remove duplicates across multiple keyword passes
    unique_jobs = list({v['url']: v for v in aggregated_jobs}.values())
    send_email_digest(unique_jobs)