import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()


class EmailSender:
    """Email sending utility"""
    
    def __init__(self):
        self.smtp_server = os.getenv('EMAIL_SMTP', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_PORT', 587))
        self.sender_email = os.getenv('EMAIL_USER')
        self.sender_password = os.getenv('EMAIL_PASS')
    
    def send_email(self, to_emails, subject, body, attachment_path=None):
        """
        Send email with optional attachment
        
        Args:
            to_emails: List of recipient emails or single email string
            subject: Email subject
            body: Email body (can be HTML)
            attachment_path: Optional file path to attach
        
        Returns:
            Boolean indicating success
        """
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = ', '.join(to_emails) if isinstance(to_emails, list) else to_emails
            message['Subject'] = subject
            
            # Add body
            message.attach(MIMEText(body, 'html'))
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as file:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                message.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✓ Email sent successfully to {message['To']}")
            return True
            
        except Exception as e:
            print(f"✗ Email sending failed: {e}")
            return False


# Example usage
if __name__ == "__main__":
    sender = EmailSender()
    
    html_body = """
    <html>
        <body>
            <h2>Test Report</h2>
            <p>This is a test email from the automated reporting system.</p>
        </body>
    </html>
    """
    
    sender.send_email(
        to_emails=['recipient@example.com'],
        subject='Test Email',
        body=html_body
    )
