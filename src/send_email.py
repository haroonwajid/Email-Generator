import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import requests  # To interact with Google Apps Script for tracking URL generation
from dotenv import load_dotenv
import os

load_dotenv()

# Load email data
data = pd.read_csv('data/mail.csv')

# Gmail credentials
gmail_user = os.getenv("GMAIL_USER")  
app_password = os.getenv("APP_PASSWORD")

# Google Apps Script endpoint for generating tracking pixels
TRACKING_SCRIPT_URL = "https://script.google.com/macros/s/your_script_id/exec"

def get_tracking_url(customer_id):
    """Generate tracking URL using Google Apps Script."""
    try:
        response = requests.get(f"{TRACKING_SCRIPT_URL}?id={customer_id}")
        if response.status_code == 200:
            return response.text  # Assuming the script returns the URL as plain text
        else:
            raise ValueError(f"Error in tracking URL generation: {response.status_code}")
    except Exception as e:
        print(f"Failed to fetch tracking URL for Customer ID {customer_id}: {str(e)}")
        return None

def send_emails(start_row, number_of_sends):
    """Sends emails from start_row to (start_row + number_of_sends) in the data."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, app_password)

    for i in range(start_row, start_row + number_of_sends):
        if i >= len(data):
            break

        row = data.iloc[i]
        customer_id = row['Customer ID']
        email_address = row['Email Address']
        subject = row['Subject Line']
        email_body = row['Email Body']

        if pd.notna(email_address) and pd.notna(subject) and pd.notna(email_body):
            try:
                # Fetch the tracking pixel URL
                tracking_pixel_url = get_tracking_url(customer_id)
                if not tracking_pixel_url:
                    print(f"Skipping Customer ID {customer_id} due to tracking URL error.")
                    continue

                tracking_pixel = f'<img src="{tracking_pixel_url}" width="1" height="1" style="display:none;">'
                html_body = f"{email_body}{tracking_pixel}"

                # Construct email
                msg = MIMEMultipart('alternative')
                msg['From'] = gmail_user
                msg['To'] = email_address
                msg['Subject'] = subject

                # Attach plain text version
                msg.attach(MIMEText(email_body, 'plain'))

                # Attach HTML version
                msg.attach(MIMEText(html_body, 'html'))

                # Send email
                server.sendmail(gmail_user, email_address, msg.as_string())
                print(f"Email sent to {email_address} (Customer ID: {customer_id})")
            except Exception as e:
                print(f"Failed to send email to {email_address}: {str(e)}")
        else:
            print(f"Skipping row {i}: Missing data")

    server.quit()

# Example Usage
send_emails(0, 5)  # Send emails starting from row 0 for 5 customers