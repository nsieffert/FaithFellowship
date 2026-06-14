from flask import Flask, render_template, redirect, jsonify, url_for, flash
from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sqlite3

# deactivate the items for email and try a database instead - secret, email key, pwd key
# import secret
# Load Gmail credentials from environment variables for security
# EMAIL_KEY = os.getenv(secret.EMAIL_KEY)
# PASSWORD_KEY = os.getenv(secret.PASSWORD_KEY)


app = Flask(__name__)
application = app
app.secret_key = 'supercalifrag' # Required for flash messages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            # Grab the data from the HTML form
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # Connect to SQLite database (creates file if it doesn't exist)
            conn = sqlite3.connect('messages.db')
            cur = conn.cursor()

            # Create table if it does not exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     email TEXT NOT NULL,
                     message TEXT NOT NULL,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                        ''')

            # Insert form data into table
            cur.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))

            # Save changes and close the connection
            conn.commit()
            conn.close()

            # Return a successful JSON response
            return jsonify({'status': 'success', 'message': 'Your message has been sent!'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500

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

@app.route('/daily-verse')
def daily_verse():
    return render_template('daily-verse.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route("/form")
def form():
    # Serve the HTML form directly
    with open("contact.html", "r") as f:
        return f.read()

# @app.route("/send", methods=["POST"])
# def send_email():
#         name = request.form.get("name")
#         email = request.form.get("email")
#         message = request.form.get("message")

#         if not all([name, email, message]):
#             return "All fields are required.", 400
#
#         # Create the email - deactivate from here to try database
#         msg = MIMEMultipart()
#         msg["From"] = secret.EMAIL_KEY
#         msg["To"] = secret.EMAIL_KEY  # Send to yourself
#         msg["Subject"] = f"New Contact Form Submission from {name}"
#
#         body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
#         msg.attach(MIMEText(body, "plain"))
#
#         # Send via Gmail SMTP
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(secret.EMAIL_KEY, secret.PASSWORD_KEY)
#             server.send_message(msg)
#             # msg["Cc"] = email_from_form - not quite sure how this works yet.
#
#         return jsonify({"status": "success", "message": "Your message has been sent successfully!"})
#
#

if __name__ == '__main__':
    app.run(debug=True)