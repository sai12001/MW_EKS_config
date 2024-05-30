import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def send_email(subject, body, to_email, from_email, from_email_password):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # The body and the attachments for the mail
    message.attach(MIMEText(body, 'plain'))

    # SMTP server configuration
    server = smtplib.SMTP_SSL('smtppro.zoho.com', 465)
    server.login(from_email, from_email_password)
    text = message.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

if __name__ == "__main__":
    # Define email parameters
    to_email = "alert@naethra.com"
    from_email = "admin@maintwiz.com"
    from_email_password = "Tv62chn@99"

    while True:
        cpu_usage = get_cpu_usage()
        if cpu_usage > 10:
            subject = "High CPU Usage Alert"
            body = f"Warning: CPU usage has exceeded 70%. Current usage: {cpu_usage}%"
            send_email(subject, body, to_email, from_email, from_email_password)
        
        # Wait for a specified amount of time before checking again
        time.sleep(60)  # Check every minute
