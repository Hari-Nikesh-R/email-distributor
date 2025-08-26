# Bulk Email Sender

A Python-based bulk email sender that uses Gmail SMTP to send personalized HTML emails with embedded images and file attachments.

## Features

- 📧 **Bulk Email Sending**: Send emails to multiple recipients from a CSV file
- 🎨 **HTML Templates**: Use Jinja2 templates with dynamic content
- 🖼️ **Embedded Images**: Automatically embed images from assets folder
- 📎 **File Attachments**: Attach files from attachments folder to all emails
- ⏱️ **Rate Limiting**: Configurable delay between emails to avoid spam filters
- 🔐 **Secure**: Uses Gmail's secure SMTP with App Passwords
- 📊 **Progress Tracking**: Real-time progress updates during sending

## Project Structure

```
email_sender/
├── venv/                    # Python virtual environment
├── assets/                  # Images and assets for templates
│   ├── logo.png            # Company logo (replace with actual image)
│   └── README.md           # Assets documentation
├── attachments/             # Files to attach to all emails
│   ├── sample_document.pdf # Sample attachment (replace with actual file)
│   └── README.md           # Attachments documentation
├── template.html            # HTML email template with Jinja2 variables
├── emails.csv               # Recipient list with email, name, company
├── email_sender.py          # Main Python script
├── requirements.txt         # Python dependencies
├── env_example.txt          # Environment variables template
└── README.md               # This file
```

## Setup Instructions

### 1. Activate Virtual Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gmail Credentials

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to [Google Account settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate a password
3. **Create `.env` file**:
   ```bash
   cp env_example.txt .env
   ```
4. **Edit `.env`** with your credentials:
   ```
   GMAIL_EMAIL=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_16_character_app_password
   ```

### 4. Customize Your Content

- **Template**: Edit `template.html` with your email content
- **Recipients**: Update `emails.csv` with your recipient list
- **Assets**: Replace placeholder files in `assets/` folder
- **Attachments**: Add files to `attachments/` folder

## Usage

### Basic Usage

```bash
python email_sender.py
```

### Customize Email Content

The `template.html` file uses Jinja2 templating with these variables:
- `{{ recipient_name }}` - Recipient's name from CSV
- `{{ company_name }}` - Recipient's company from CSV

### CSV Format

Your `emails.csv` should have these columns:
```csv
email,name,company
john@example.com,John Doe,ABC Company
jane@example.com,Jane Smith,XYZ Corp
```

### Adding Images

1. Place images in the `assets/` folder
2. Reference them in your template using `cid:filename`:
   ```html
   <img src="cid:logo" alt="Company Logo">
   ```

### Adding Attachments

1. Place files in the `attachments/` folder
2. All files will be automatically attached to every email
3. Supported formats: PDF, DOC, DOCX, TXT, PNG, JPG, etc.

## Configuration Options

### Email Delay

Modify the delay between emails in `email_sender.py`:
```python
successful, total = sender.send_bulk_emails(delay_seconds=5)  # 5 second delay
```

### SMTP Settings

Default settings (Gmail):
- Server: `smtp.gmail.com`
- Port: `587`
- Security: TLS

## Troubleshooting

### Common Issues

1. **Authentication Error**:
   - Ensure 2FA is enabled
   - Use App Password, not regular password
   - Check `.env` file exists and has correct credentials

2. **Template Not Found**:
   - Verify `template.html` exists in project root
   - Check file permissions

3. **CSV File Error**:
   - Ensure `emails.csv` has correct format
   - Check column headers match expected format

4. **Gmail Blocking**:
   - Reduce delay between emails
   - Check Gmail sending limits
   - Verify account isn't flagged for spam

### Gmail Limits

- **Daily sending limit**: 500 emails per day
- **Rate limit**: ~20 emails per minute recommended
- **App Password**: Required for 2FA-enabled accounts

## Security Notes

- ⚠️ **Never commit `.env` file** to version control
- 🔐 **Use App Passwords**, not regular passwords
- 📧 **Respect email regulations** and anti-spam laws
- ⏱️ **Add delays** to avoid triggering spam filters

## Customization

### Adding New Template Variables

1. Add columns to `emails.csv`
2. Update template rendering in `email_sender.py`:
   ```python
   html_content = template.render(
       recipient_name=recipient_data['name'],
       company_name=recipient_data['company'],
       new_field=recipient_data['new_field']  # Add new variable
   )
   ```

### Conditional Attachments

Modify `attach_files()` method to add conditional logic based on recipient data.

### Different Templates per Recipient

Extend the script to select different templates based on recipient criteria.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Include type hints where appropriate
- Write tests for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that allows for:
- Commercial use
- Modification
- Distribution
- Private use

While providing liability protection for the authors.

## Disclaimer

This software is provided "as is" without warranty. Users are responsible for:
- Complying with email regulations and anti-spam laws in their jurisdiction
- Obtaining proper consent from email recipients
- Following Gmail's terms of service and sending limits
- Ensuring their use case is legal and ethical

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all setup steps are completed
3. Check Gmail account settings and limits
4. Review error messages for specific guidance
5. Open an issue on GitHub for bugs or feature requests
# email-distributor
