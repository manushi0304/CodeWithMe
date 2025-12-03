import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_weekly_email(to_email, roadmap_text):
    msg = EmailMessage()
    msg.set_content(f"Hello! Here's your personalized weekly plan:\n\n{roadmap_text}")
    msg['Subject'] = "Your CodeMate Weekly Plan "
    msg['From'] = EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        return str(e)