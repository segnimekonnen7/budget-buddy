import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os

FILENAME = "top_resumes.csv"

# Hardcoded email config
SENDER = "grimes2020rick@gmail.com"
PASSWORD = "lbgl rpkm okbp soan"
RECIPIENT = "grimes2020rick@gmail.com"

def send_email_with_attachment(sender, password, recipient, subject, body, filename):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with open(filename, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
        msg.attach(part)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email_with_attachment(
        SENDER, PASSWORD, RECIPIENT,
        "Top AI/ML Resumes & Portfolios",
        "See attached CSV for results.",
        FILENAME
    ) 