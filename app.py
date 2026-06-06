from flask import Flask, render_template, redirect, jsonify
from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

import secret

# Load Gmail credentials from environment variables for security
EMAIL_KEY = os.getenv(secret.EMAIL_KEY)
PASSWORD_KEY = os.getenv(secret.PASSWORD_KEY)


app = Flask(__name__)
application = app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/watch')
def watch():
    return render_template('watch.html')

@app.route('/give')
def give():
    return render_template('give.html')

@app.route('/believe')
def believe():
    return render_template('believe.html')

@app.route('/studies')
def studies():
    return render_template('studies.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route("/form")
def form():
    # Serve the HTML form directly
    with open("contact.html", "r") as f:
        return f.read()

@app.route("/send", methods=["POST"])
def send_email():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not all([name, email, message]):
            return "All fields are required.", 400

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = secret.EMAIL_KEY
        msg["To"] = secret.EMAIL_KEY  # Send to yourself
        msg["Subject"] = f"New Contact Form Submission from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, "plain"))

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(secret.EMAIL_KEY, secret.PASSWORD_KEY)
            server.send_message(msg)
            # msg["Cc"] = email_from_form - not quite sure how this works yet.

        return jsonify({"status": "success", "message": "Your message has been sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error sending message: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
