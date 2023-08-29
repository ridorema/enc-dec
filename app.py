from flask import Flask, render_template, request
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
from helpers import  encrypt_file, decrypt_file, send_encrypted_email_with_key


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


#@app.route('/generate_password', methods=['GET', 'POST'])
#def generate_password_route():
 #   if request.method == 'POST':
  #      # Generate password
   #     password = generate_password()

        # Send password via email
 #       recipient_email = request.form['email']
  #      send_password_email(recipient_email, password)

   #     return render_template('password_generated.html', password=password)
    #return render_template('generate_password.html')


# Generate a Fernet key once when the app starts
fernet_key = Fernet.generate_key()

@app.route('/encrypt_file', methods=['GET', 'POST'])
def encrypt_file_route():
    if request.method == 'POST':
        # Encrypt file and send encrypted file via email along with the key
        recipient_email = request.form['recipient_email']
        uploaded_file = request.files['file']

        encrypted_file = encrypt_file(uploaded_file, fernet_key)

        # Save the Fernet key to a temporary file
        key_filename = 'encryption_key.key'
        with open(key_filename, 'wb') as key_file:
            key_file.write(fernet_key)

        send_encrypted_email_with_key(recipient_email, encrypted_file, key_filename)

        return render_template('file_encrypted.html')
    return render_template('encrypt_file.html')

@app.route('/decrypt_file', methods=['GET', 'POST'])
def decrypt_file_route():
    if request.method == 'POST':
        # Decrypt file using the provided key
        uploaded_file = request.files['file']
        decryption_key = request.form['key']

        decrypted_file = decrypt_file(uploaded_file, decryption_key)

        return render_template('file_decrypted.html', decrypted_file=decrypted_file)
    return render_template('decrypt_file.html')


if __name__ == '__main__':
    app.run(debug=True)
