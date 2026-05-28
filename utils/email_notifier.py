import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
NOTIFY_TO_EMAIL = os.getenv("NOTIFY_TO_EMAIL")


def send_job_notification(jobs):
    if not jobs:
        return "No jobs to send."

    body = "New IT jobs found:\n\n"

    for job in jobs[:5]:
        body += f"""
Role: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Posted: {job.get('created')}
Apply: {job.get('apply_link')}

------------------------
"""

    msg = MIMEText(body)
    msg["Subject"] = "New IT Job Alerts - AI Career Copilot"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = NOTIFY_TO_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            server.send_message(msg)

        return "Email notification sent successfully."

    except Exception as e:
        return f"Email error: {e}"