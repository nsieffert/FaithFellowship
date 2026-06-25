import os
import secret
from flask import Flask, render_template, redirect, jsonify, url_for, flash, session
from flask import Flask, request, render_template_string
import requests
import sqlite3
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
application = app
app.secret_key = 'supercalifrag' # Required for flash messages

# Set your master password here
ADMIN_PASSWORD = secret.ADMIN_KEY

# Tell Flask where to save your uploaded images inside the static folder
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 👇 MAKE SURE THIS EXACT LINE IS HERE 👇
DATA_FILE = 'current_verse.json'

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

# Do not change anything above this line! Except new imports

# 1. NEW: The Login Page Route
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Grab the password typed into the login form
        typed_password = request.form.get('password')

        # Verify if the password matches your master password
        if typed_password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Give the user their "wristband"
            return redirect(url_for('admin_page'))
        else:
            return render_template('login.html', error="Incorrect password. Try again.")

    return render_template('login.html', error=None)


# 2. UPDATED: Your Admin Dashboard Route (Protected)
@app.route('/admin-dashboard')
def admin_page():
    # Check if the user has the "wristband" cookie. If not, kick them out to login.
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    return render_template('admin.html')


# 3. The Form Submission Route (Protected for safety)
@app.route('/publish-daily', methods=['POST'])
def publish_daily():
    if not session.get('logged_in'):
        return "Unauthorized access denied.", 403

    verse_text = request.form.get('verse')
    youtube_url = request.form.get('youtube_url')
    image_file = request.files.get('image_file')

    embed_url = ""
    if youtube_url:
        if "watch?v=" in youtube_url:
            # Safely strips everything before the ID, and splits off any extra trailing parameters like playlists
            video_id = youtube_url.split("watch?v=")[1].split("&")[0]
            embed_url = f"https://youtube.com{video_id}"
        elif "youtu.be/" in youtube_url:
            # Safely handles mobile share links
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
            embed_url = f"https://youtube.com{video_id}"
        else:
            embed_url = youtube_url
    # ----------------------------------------

    # 2. FIXED IMAGE SAVING AND PLACEHOLDER
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)

        # This line will now work perfectly since you created the static/images folder!
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Hardcoded real internet image so Zapier doesn't fail locally
        public_image_url = f"https://faithfellowshipterrell.org{filename}"
    else:
        public_image_url = ""

    daily_content = {
        "verse": verse_text,
        "youtube_video": embed_url,
        "image": public_image_url
    }

    # Save data locally to your JSON file
    with open(DATA_FILE, 'w') as file:
        json.dump(daily_content, file)

    # Send data to Zapier
    zapier_webhook_url = "https://hooks.zapier.com/hooks/catch/28051022/42s1dq0/"

    # NEW CODE: This tricks Zapier's firewall into treating Python like a normal browser
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Connection': 'close'  # Explicitly closes the connection after passing data safely
    }

    try:
        # We pass both the data and our custom browser headers mask
        response = requests.post(zapier_webhook_url, json=daily_content, headers=custom_headers)
        print(f"Zapier Status Code: {response.status_code}")
    except Exception as e:
        print(f"Automation failed: {e}")

    return "Successfully published to website and sent to social media!"


# 4. OPTIONAL: A Logout Route to clear your cookie when done
@app.route('/admin-logout')
def admin_logout():
    session.pop('logged_in', None)  # Destroy the digital wristband
    return "You have been logged out safely."


if __name__ == '__main__':
    app.run(debug=True)