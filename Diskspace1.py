import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_disk_usage():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition.device == '/dev/nvme0n1p1':
            usage = psutil.disk_usage(partition.mountpoint)
            total_space = usage.total / (1024 ** 3)  # Convert from bytes to GB
            used_space = usage.used / (1024 ** 3)  # Convert from bytes to GB
            free_space = usage.free / (1024 ** 3)  # Convert from bytes to GB
            percent_usage = usage.percent

            return percent_usage, total_space, used_space, free_space
    return None, None, None, None

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
    percent_usage, total_space, used_space, free_space = get_disk_usage()
    if percent_usage is not None:
        subject = "Live App Server Disk Space"
        body = (
            f"Disk Usage: {percent_usage:.2f}%\n"
            f"Total Space: {total_space:.2f} GB\n"
            f"Used Space: {used_space:.2f} GB\n"
            f"Available Space: {free_space:.2f} GB"
        )
        to_email = "alert@naethra.com"
        from_email = "admin@maintwiz.com"
        from_email_password = "Tv62chn@99"
        send_email(subject, body, to_email, from_email, from_email_password)
    else:
        print("Partition /dev/nvme0n1p1 not found.")