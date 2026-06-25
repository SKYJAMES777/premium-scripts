#!/usr/bin/env python3
"""Email Campaign Manager - Send personalized bulk emails via SMTP.
Price: $20"""
import smtplib, csv, sys
from email.mime.text import MIMEText
def send_campaign(smtp_host, smtp_port, username, password, csv_file):
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            msg = MIMEText(row.get("message", "Hello"), "plain", "utf-8")
            msg["Subject"] = row.get("subject", "Hello")
            msg["From"] = username; msg["To"] = row["email"]
            with smtplib.SMTP(smtp_host, smtp_port) as s:
                s.starttls(); s.login(username, password); s.send_message(msg)
            print("Sent to %s" % row["email"])
if __name__ == "__main__":
    print("Usage: python email_campaign.py <smtp_host> <port> <user> <pass> <emails.csv>")
