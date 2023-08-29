import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from password_generator import generate_password

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'doriremanica27@gmail.com'
SMTP_PASSWORD = 'prcvpraodhlxetpv'
RECIPIENT_EMAIL = input("Enter your email address: ")


def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
    server.quit()


if __name__ == "__main__":
    while True:
        password = generate_password()
        print("Generated password:", password)

        subject = "Generated Password"
        body = "Your generated password: " + password
        send_email(subject, body)

        choice = input("Generate another password? (y/n): ")
        if choice.lower() != 'y':
            break
