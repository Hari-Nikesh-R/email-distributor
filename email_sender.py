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
        self.sent_emails_log = "sent_emails.log"
        
    def load_template(self):
        """Load and return the HTML template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as file:
                return Template(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
    
    def load_sent_emails(self):
        """Load list of already sent emails from log file"""
        sent_emails = set()
        try:
            with open(self.sent_emails_log, 'r', encoding='utf-8') as file:
                for line in file:
                    email = line.strip()
                    if email and '@' in email:
                        sent_emails.add(email)
        except FileNotFoundError:
            # Log file doesn't exist yet, that's fine
            pass
        return sent_emails
    
    def mark_email_as_sent(self, email):
        """Mark an email as sent by adding it to the log file"""
        try:
            with open(self.sent_emails_log, 'a', encoding='utf-8') as file:
                file.write(f"{email}\n")
        except Exception as e:
            print(f"Warning: Could not log sent email {email}: {e}")
    
    def load_recipients(self):
        """Load recipient data from CSV file and filter out already sent emails"""
        all_recipients = []
        try:
            with open(self.emails_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    all_recipients.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Emails CSV file not found: {self.emails_csv_path}")
        
        # Load already sent emails
        sent_emails = self.load_sent_emails()
        
        # Filter out already sent emails
        new_recipients = []
        already_sent = []
        
        for recipient in all_recipients:
            if recipient['email'] in sent_emails:
                already_sent.append(recipient)
            else:
                new_recipients.append(recipient)
        
        return new_recipients, already_sent
    
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
    
    def send_email(self, recipient_data, include_attachments=True):
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
                recipient_name=recipient_data.get('name', 'Valued Member'),
                company_name=recipient_data.get('company', 'Tamil Nadu JUG'),
                event_date=recipient_data.get('event_date', 'August 30, 2025'),
                event_venue=recipient_data.get('event_venue', 'Kongu Engineering College'),
                event_time=recipient_data.get('event_time', '9:00 AM – 4:00 PM')
            )
            
            # Embed images
            html_content = self.embed_images(message, html_content)
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Attach files only if requested
            if include_attachments:
                self.attach_files(message)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Create SSL context with proper certificate verification
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                server.starttls(context=ssl_context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            # Mark email as sent
            self.mark_email_as_sent(recipient_data['email'])
            print(f"✓ Email sent successfully to {recipient_data['email']}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email to {recipient_data['email']}: {e}")
            return False
    
    def send_bulk_emails(self, delay_seconds=2):
        """Send emails to all recipients with optional delay"""
        new_recipients, already_sent = self.load_recipients()
        total_new_recipients = len(new_recipients)
        total_already_sent = len(already_sent)
        
        print(f"Starting bulk email campaign...")
        print(f"📊 Recipient Summary:")
        print(f"   New recipients: {total_new_recipients}")
        print(f"   Already sent: {total_already_sent}")
        print(f"   Total in CSV: {total_new_recipients + total_already_sent}")
        print(f"⏱️  Delay between emails: {delay_seconds} seconds")
        
        # Show already sent emails
        if already_sent:
            print(f"\n📤 Already sent emails (will be skipped):")
            for recipient in already_sent:
                print(f"   - {recipient['email']} ({recipient['name']})")
        
        # Check if there are new recipients to send to
        if total_new_recipients == 0:
            print("\n✅ All emails have already been sent!")
            print("💡 To send emails again, you can:")
            print("   1. Add new email addresses to emails.csv")
            print("   2. Delete sent_emails.log to reset the tracking")
            return 0, 0
        
        # Ask user about attachments
        print(f"\n📎 Attachment Options:")
        print("1. Send emails with attachments")
        print("2. Send emails without attachments")
        
        while True:
            attachment_choice = input("\n🤔 Do you want to include attachments? (1/2): ").strip()
            if attachment_choice in ['1', '2']:
                include_attachments = attachment_choice == '1'
                break
            else:
                print("❌ Please enter 1 or 2")
        
        if include_attachments:
            print("✅ Attachments will be included in emails")
            # Check if attachments folder has files
            attachments_path = Path(self.attachments_folder)
            if attachments_path.exists():
                attachment_files = [f for f in attachments_path.iterdir() 
                                  if f.is_file() and f.name != 'README.md']
                if attachment_files:
                    print(f"📁 Found {len(attachment_files)} attachment(s):")
                    for file in attachment_files:
                        print(f"   - {file.name}")
                else:
                    print("⚠️  Attachments folder is empty")
            else:
                print("⚠️  Attachments folder not found")
        else:
            print("❌ Attachments will NOT be included in emails")
        
        print("-" * 50)
        
        successful_sends = 0
        for i, recipient in enumerate(new_recipients, 1):
            print(f"Processing {i}/{total_new_recipients}: {recipient['email']}")
            
            if self.send_email(recipient, include_attachments):
                successful_sends += 1
            
            # Add delay between emails (except for the last one)
            if i < total_new_recipients and delay_seconds > 0:
                print(f"Waiting {delay_seconds} seconds...")
                time.sleep(delay_seconds)
        
        print("-" * 50)
        print(f"Campaign completed!")
        print(f"Successful sends: {successful_sends}/{total_new_recipients}")
        
        return successful_sends, total_new_recipients

def main():
    """Main function to run the bulk email sender"""
    try:
        # Create email sender instance
        sender = BulkEmailSender()
        
        # Send bulk emails (attachment choice will be prompted during execution)
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
