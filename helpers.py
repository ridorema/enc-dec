import random
import string
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from flask import current_app
from config import Config
from email.mime.base import MIMEBase


# Helper function to generate a random password
#def generate_password(length=16):
 #   characters = string.ascii_letters + string.digits + string.punctuation
  #  password = ''.join(random.choice(characters) for _ in range(length))
   # return password


# Helper function to send an email with a generated password
#def send_password_email(recipient_email, password):
 #   subject = "Generated Password"
  #  body = f"Your generated password: {password}"
   # send_email(recipient_email, subject, body)





# Helper function to send an email with an encrypted file and the key attached
def send_encrypted_email_with_key(recipient_email, encrypted_file, key_filename):
    subject = "Encrypted File and Key"
    body = "The encrypted file is attached. The key is attached as a separate file."
    send_email(recipient_email, subject, body, attachments=[encrypted_file, key_filename])



# Helper function to send email
def send_email(recipient_email, subject, body, attachments=['static/encrypted/'],
           from_email='your_email@gmail.com', email_password='your app email_password'):
    if not from_email or not email_password:
        raise ValueError("Email credentials are required.")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for attachment_path in attachments:
            with open(attachment_path, "rb") as f:
                attachment_data = f.read()
                attachment_part = MIMEBase('application', 'octet-stream')
                attachment_part.set_payload(attachment_data)
                attachment_part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
                msg.attach(attachment_part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, email_password)
    server.sendmail(from_email, recipient_email, msg.as_string())
    server.quit()


# Helper function to encrypt a file
def encrypt_file(file, key):
    cipher_suite = Fernet(key)

    file_contents = file.read()
    encrypted_data = cipher_suite.encrypt(file_contents)

    encrypted_file_directory = 'static/encrypted/'
    if not os.path.exists(encrypted_file_directory):
        os.makedirs(encrypted_file_directory)

    encrypted_file_path = os.path.join(encrypted_file_directory, file.filename + '.encrypted')
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    return encrypted_file_path

# Helper function to decrypt a file using a given key
def decrypt_file(file, key):
    cipher_suite = Fernet(key)

    encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    decrypted_file_directory = 'static/decrypted/'
    if not os.path.exists(decrypted_file_directory):
        os.makedirs(decrypted_file_directory)

    decrypted_file_path = os.path.join(decrypted_file_directory, f'{file.filename}.decrypted')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    return decrypted_file_path