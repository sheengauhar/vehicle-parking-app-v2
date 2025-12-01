import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 

SMTP_HOST = 'localhost'
SMTP_PORT = 1025 
FROM_EMAIL = 'admin@vehicleparkingapp.com'

def send_email(to_email, subject, body, attachments=None):
    msg = MIMEMultipart()
    msg[ "Subject"] = subject
    msg[ 'From'] = FROM_EMAIL
    msg['To'] = to_email

    msg.attach(MIMEText(body, "html"))

    if attachments:
        for filename, content in attachments:
            part = MIMEApplication(content, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")