#!/usr/bin/env python3
"""
Bulk Email Sender using Gmail SMTP
Supports HTML templates, embedded images, and file attachments
"""

import os
import smtplib
import csv
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from jinja2 import Template
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BulkEmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('GMAIL_EMAIL')
        self.sender_password = os.getenv('GMAIL_APP_PASSWORD')
        
        # Validate credentials
        if not self.sender_email or not self.sender_password:
            raise ValueError("GMAIL_EMAIL and GMAIL_APP_PASSWORD must be set in .env file")
        
        self.template_path = "template.html"
        self.emails_csv_path = "emails.csv"
        self.assets_folder = "assets"
        self.attachments_folder = "attachments"
        
    def load_template(self):
        """Load and return the HTML template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as file:
                return Template(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
    
    def load_recipients(self):
        """Load recipient data from CSV file"""
        recipients = []
        try:
            with open(self.emails_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    recipients.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Emails CSV file not found: {self.emails_csv_path}")
        
        return recipients
    
    def embed_images(self, message, html_content):
        """Embed images from assets folder into the email"""
        assets_path = Path(self.assets_folder)
        if not assets_path.exists():
            return html_content
        
        # Find all image files in assets folder
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        for file_path in assets_path.iterdir():
            if file_path.suffix.lower() in image_extensions:
                try:
                    with open(file_path, 'rb') as img_file:
                        img_data = img_file.read()
                        img_mime = MIMEImage(img_data)
                        img_mime.add_header('Content-ID', f'<{file_path.stem}>')
                        message.attach(img_mime)
                except Exception as e:
                    print(f"Warning: Could not embed image {file_path}: {e}")
        
        return html_content
    
    def attach_files(self, message):
        """Attach files from attachments folder"""
        attachments_path = Path(self.attachments_folder)
        if not attachments_path.exists():
            return
        
        # Find all files in attachments folder
        for file_path in attachments_path.iterdir():
            if file_path.is_file() and file_path.name != 'README.md':
                try:
                    with open(file_path, 'rb') as attachment_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment_file.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.name}'
                    )
                    message.attach(part)
                    print(f"Attached: {file_path.name}")
                except Exception as e:
                    print(f"Warning: Could not attach file {file_path}: {e}")
    
    def send_email(self, recipient_data):
        """Send a single email to a recipient"""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = recipient_data['email']
            message['Subject'] = f"Welcome to Our Company, {recipient_data['name']}!"
            
            # Load and render template
            template = self.load_template()
            html_content = template.render(
                recipient_name=recipient_data['name'],
                company_name=recipient_data['company']
            )
            
            # Embed images
            html_content = self.embed_images(message, html_content)
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Attach files
            self.attach_files(message)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✓ Email sent successfully to {recipient_data['email']}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email to {recipient_data['email']}: {e}")
            return False
    
    def send_bulk_emails(self, delay_seconds=2):
        """Send emails to all recipients with optional delay"""
        recipients = self.load_recipients()
        total_recipients = len(recipients)
        successful_sends = 0
        
        print(f"Starting bulk email campaign...")
        print(f"Total recipients: {total_recipients}")
        print(f"Delay between emails: {delay_seconds} seconds")
        print("-" * 50)
        
        for i, recipient in enumerate(recipients, 1):
            print(f"Processing {i}/{total_recipients}: {recipient['email']}")
            
            if self.send_email(recipient):
                successful_sends += 1
            
            # Add delay between emails (except for the last one)
            if i < total_recipients and delay_seconds > 0:
                print(f"Waiting {delay_seconds} seconds...")
                time.sleep(delay_seconds)
        
        print("-" * 50)
        print(f"Campaign completed!")
        print(f"Successful sends: {successful_sends}/{total_recipients}")
        
        return successful_sends, total_recipients

def main():
    """Main function to run the bulk email sender"""
    try:
        # Create email sender instance
        sender = BulkEmailSender()
        
        # Send bulk emails
        successful, total = sender.send_bulk_emails(delay_seconds=2)
        
        if successful == total:
            print("🎉 All emails sent successfully!")
        else:
            print(f"⚠️  {total - successful} emails failed to send")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your .env file has GMAIL_EMAIL and GMAIL_APP_PASSWORD")
        print("2. Ensure you have 2FA enabled and are using an App Password")
        print("3. Check your Gmail settings allow less secure app access")
        print("4. Verify all required files exist (template.html, emails.csv)")

if __name__ == "__main__":
    main()
